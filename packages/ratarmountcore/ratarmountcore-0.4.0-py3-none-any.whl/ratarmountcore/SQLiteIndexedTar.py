#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import json
import multiprocessing.pool
import os
import platform
import re
import sqlite3
import stat
import sys
import tarfile
import threading
import time
import traceback
import urllib.parse

from timeit import default_timer as timer
from typing import Any, AnyStr, Callable, cast, Dict, Generator, IO, Iterable, List, Optional, Tuple, Union
from dataclasses import dataclass

try:
    import indexed_bzip2
except ImportError:
    pass

try:
    import indexed_gzip
except ImportError:
    pass

try:
    import pragzip
except ImportError:
    pass

try:
    import xz
except ImportError:
    xz = None  # type: ignore

from .version import __version__
from .MountSource import FileInfo, MountSource
from .ProgressBar import ProgressBar
from .SQLiteBlobFile import SQLiteBlobsFile, WriteSQLiteBlobs
from .StenciledFile import StenciledFile
from .compressions import findAvailableOpen, getGzipInfo, TAR_COMPRESSION_FORMATS
from .utils import (
    RatarmountError,
    IndexNotOpenError,
    InvalidIndexError,
    CompressionError,
    ceilDiv,
    findModuleVersion,
    overrides,
)
from .BlockParallelReaders import ParallelXZReader


class _TarFileMetadataReader:
    def __init__(
        self,
        parent: 'SQLiteIndexedTar',
        _setFileInfos: Callable[[List[Tuple]], None],
        _updateProgressBar: Callable[[], None],
    ):
        self._parent = parent
        self._setFileInfos = _setFileInfos
        self._updateProgressBar = _updateProgressBar

        self._lastUpdateTime = time.time()

        self._futures: List[multiprocessing.pool.AsyncResult] = []
        self._filesToMountRecursively: List[Tuple] = []
        self._fileInfos: List[Tuple] = []

    @staticmethod
    def _getTarPrefix(fileObject: IO[bytes], tarInfo: tarfile.TarInfo, printDebug: int) -> Optional[bytes]:
        """Get the actual prefix as stored in the TAR."""

        # Offsets taken from https://en.wikipedia.org/wiki/Tar_(computing)#UStar_format
        def extractPrefix(tarBlockOffset):
            fileObject.seek(tarBlockOffset + 345)
            return fileObject.read(155)

        def extractName(tarBlockOffset):
            fileObject.seek(tarBlockOffset)
            return fileObject.read(100)

        def extractSize(tarBlockOffset):
            fileObject.seek(tarBlockOffset + 124)
            return int(fileObject.read(12).strip(b"\0"), 8)  # octal encoded file size TODO might also be base64

        oldPosition = fileObject.tell()

        # Normally, getting the prefix, could be as easy as calling extractPrefix.
        # But, for long-names the prefix will not be prefixed but for long links it will be prefixed by tarfile.
        # This complicates things. Also, both long link and long name are implemented by a prepended
        # tar block with the special file name "././@LongLink" and tarfile will return the header offset of the
        # corresponding GNU LongLink file header in the TarInfo object instead of the actual file header, which
        # contains the prefix.
        try:
            if extractName(tarInfo.offset).startswith(b"././@LongLink\0"):
                nextHeaderOffset = tarInfo.offset + 512 + (extractSize(tarInfo.offset) + 512 - 1) // 512 * 512
                return extractPrefix(nextHeaderOffset)
            return extractPrefix(tarInfo.offset)

        except Exception as exception:
            if printDebug >= 1:
                print("[Warning] Encountered exception when trying to get TAR prefix", exception)
            if printDebug >= 3:
                traceback.print_exc()

        finally:
            fileObject.seek(oldPosition)

        return None

    @staticmethod
    def _tarInfoFullMode(tarInfo: tarfile.TarInfo) -> int:
        """
        Returns the full mode for a TarInfo object. Note that TarInfo.mode only contains the permission bits
        and not other bits like set for directory, symbolic links, and other special files.
        """

        return (
            tarInfo.mode
            # fmt: off
            | ( stat.S_IFDIR if tarInfo.isdir () else 0 )
            | ( stat.S_IFREG if tarInfo.isfile() or tarInfo.type == b'D' else 0 )
            | ( stat.S_IFLNK if tarInfo.issym () else 0 )
            | ( stat.S_IFCHR if tarInfo.ischr () else 0 )
            | ( stat.S_IFIFO if tarInfo.isfifo() else 0 )
            # fmt: on
        )

    @staticmethod
    def _fixIncrementalBackupNamePrefixes(fileObject: IO[bytes], tarInfo: tarfile.TarInfo, printDebug: int):
        """
        Tarfile joins the TAR prefix with the file path.
        However, for incremental TARs, the prefix is an octal timestamp and should be ignored.
        This function reads the raw prefix from the TAR file and removes it from the TarInfo object's path
        if the prefix is an octal number indicating an incremental archive prefix.
        """

        if '/' not in tarInfo.name:
            return

        fixedPath = None
        prefix, name = tarInfo.name.split('/', 1)

        realPrefix = _TarFileMetadataReader._getTarPrefix(fileObject, tarInfo, printDebug)
        encodedPrefix = prefix.encode('utf8', 'surrogateescape')

        # For names longer than 100B, GNU tar will store it using a ././@LongLink named file.
        # In this case, tarfile will ignore the truncated filename AND the octal timestamp prefix!
        # However, for long symbolic links, the prefix WILL be prepended to the @LongLink contents!
        # In order to not strip folders erroneously, test against this prefix. Unfortunately, this is
        # not perfect either because tarfile removes trailing slashes for names. So we have to
        # read the TAR information ourselves.
        # Note that the prefix contains two not always identical octal timestamps! E.g.,
        #   b'13666753432\x0013666377326\x00\x00\x00...
        # We only test for the first here as I'm not sure what the second one is.
        # In some cases instead of the octal timestamp there will be unknown binary data!
        # Because of this the data is not asserted to be octal.
        if realPrefix and realPrefix.startswith(encodedPrefix + b"\0"):
            fixedPath = name

        if fixedPath is None and printDebug >= 1:
            print(f"[Warning] ignored prefix '{encodedPrefix!r}' because it was not found in TAR header prefix.")
            print("[Warning]", realPrefix[:30] if realPrefix else realPrefix)
            print(f"[Info] TAR header offset: {tarInfo.offset}, type: {str(tarInfo.type)}")
            print("[Info] name:", tarInfo.name)
            print()

        if fixedPath is not None:
            tarInfo.name = fixedPath

    @staticmethod
    def _processTarInfo(
        # fmt: off
        tarInfo          : tarfile.TarInfo,
        fileObject       : IO[bytes],
        pathPrefix       : str,
        streamOffset     : int,
        isGnuIncremental : Optional[bool],
        mountRecursively : bool,
        printDebug       : int,
        # fmt: on
    ) -> Tuple[List[Tuple], bool, Optional[bool]]:
        """Postprocesses a TarInfo object into one or multiple FileInfo tuples."""

        if tarInfo.type == b'D' and not isGnuIncremental:
            isGnuIncremental = True
            if printDebug >= 1:
                print(f"[Warning] A folder metadata entry ({tarInfo.name}) for GNU incremental archives")
                print("[Warning] was encountered but this archive was not automatically recognized as such!")
                print("[Warning] Please call ratarmount with the --gnu-incremental flag if there are problems.")
                print()

        if isGnuIncremental:
            _TarFileMetadataReader._fixIncrementalBackupNamePrefixes(fileObject, tarInfo, printDebug)

        # Add a leading '/' as a convention where '/' represents the TAR root folder
        # Partly, done because fusepy specifies paths in a mounted directory like this
        # os.normpath does not delete duplicate '/' at beginning of string!
        # tarInfo.name might be identical to "." or begin with "./", which is bad!
        # os.path.normpath can remove suffixed folder/./ path specifications but it can't remove
        # a leading dot.
        # TODO: Would be a nice function / line of code to test because it is very finicky.
        #       And some cases are only triggered for recursive mounts, i.e., for non-empty pathPrefix.
        fullPath = "/" + os.path.normpath(pathPrefix + "/" + tarInfo.name).lstrip('/')

        # TODO: As for the tarfile type SQLite expects int but it is generally bytes.
        #       Most of them would be convertible to int like tarfile.SYMTYPE which is b'2',
        #       but others should throw errors, like GNUTYPE_SPARSE which is b'S'.
        #       When looking at the generated index, those values get silently converted to 0?
        path, name = fullPath.rsplit("/", 1)
        # fmt: off
        fileInfo : Tuple = (
            path                                            ,  # 0
            name                                            ,  # 1
            streamOffset + tarInfo.offset                   ,  # 2
            streamOffset + tarInfo.offset_data              ,  # 3
            tarInfo.size                                    ,  # 4
            tarInfo.mtime                                   ,  # 5
            _TarFileMetadataReader._tarInfoFullMode(tarInfo),  # 6
            tarInfo.type                                    ,  # 7
            tarInfo.linkname                                ,  # 8
            tarInfo.uid                                     ,  # 9
            tarInfo.gid                                     ,  # 10
            False                                           ,  # 11 (isTar)
            tarInfo.issparse()                              ,  # 12
        )
        # fmt: on

        fileInfos = [fileInfo]

        if mountRecursively and tarInfo.isfile() and tarInfo.name.lower().endswith('.tar'):
            return fileInfos, True, isGnuIncremental

        # Add GNU incremental TAR directory metadata files also as directories
        if tarInfo.type == b'D':
            dirFileInfo = list(fileInfo)
            # This is only to get a unique primary key :/
            # Then again, TAR blocks are known to be on 512B boundaries, so the lower
            # bits in the offset are redundant anyway.
            dirFileInfo[2] += 1
            dirFileInfo[4] = 0  # directory entries have no size by convention
            dirFileInfo[6] = tarInfo.mode | stat.S_IFDIR
            fileInfos.append(tuple(dirFileInfo))

        return fileInfos, False, isGnuIncremental

    @staticmethod
    def _readTarFiles(
        # fmt: off
        pathToTar        : str,
        startOffset      : int,
        size             : int,
        pathPrefix       : str,
        streamOffset     : int,
        isGnuIncremental : Optional[bool],
        mountRecursively : bool,
        ignoreZeros      : bool,
        encoding         : str,
        printDebug       : int,
    ):
        """
        Opens a view of the data range [startOffset, startOffset+size) of the given pathToTar and extracts
        all TAR file metadata and returns it as FileInfo tuples.
        """

        filesToMountRecursively: List[Tuple] = []
        fileInfos: List[Tuple] = []

        with open(pathToTar, 'rb') as rawFileObject:
            fileObject = cast(IO[bytes], StenciledFile([(rawFileObject, startOffset, size)]))
            try:
                loadedTarFile: Any = tarfile.open(
                    fileobj=fileObject, mode='r:', ignore_zeros=ignoreZeros, encoding=encoding
                )
            except tarfile.ReadError:
                return fileInfos, filesToMountRecursively, isGnuIncremental

            try:
                for tarInfo in loadedTarFile:
                    loadedTarFile.members = []  # Clear this in order to limit memory usage by tarfile
                    newFileInfos, mightBeTar, isGnuIncremental = _TarFileMetadataReader._processTarInfo(
                        tarInfo,
                        pathPrefix=pathPrefix,
                        streamOffset=streamOffset + startOffset,
                        fileObject=fileObject,
                        isGnuIncremental=isGnuIncremental,
                        mountRecursively=mountRecursively,
                        printDebug=printDebug,
                    )

                    if mightBeTar:
                        filesToMountRecursively.extend(newFileInfos)
                    else:
                        fileInfos.extend(newFileInfos)
            except tarfile.ReadError as e:
                if 'unexpected end of data' in str(e):
                    print(
                        "[Warning] The TAR file is incomplete. Ratarmount will work but some files might be cut off. "
                        "If the TAR file size changes, ratarmount will recreate the index during the next mounting."
                    )
                    if printDebug >= 3:
                        traceback.print_exc()

        return fileInfos, filesToMountRecursively, isGnuIncremental

    @staticmethod
    def findTarFileOffsets(fileObject: IO[bytes], ignoreZeros: bool) -> Generator[Tuple[int, bytes], None, None]:
        """
        Generator which yields offsets in the given TAR suitable for splitting the file into sub TARs.
        Also returns the type of the TAR metadata block at the returned offset for convenience.
        """

        blockNumber = 0
        skipNextBlocks = 0
        fileObject.seek(0)

        while True:
            blockContents = fileObject.read(512)
            if len(blockContents) < 512:
                break

            # > The end of an archive is marked by at least two consecutive zero-filled records.
            if blockContents == b"\0" * 512:
                blockContents = fileObject.read(512)
                if blockContents == b"\0" * 512:
                    if ignoreZeros:
                        continue
                    break

                if len(blockContents) < 512:
                    break

            typeFlag = blockContents[156:157]

            if skipNextBlocks > 0:
                skipNextBlocks -= 1
            else:
                yield blockNumber * 512, typeFlag

            blockNumber += 1
            rawSize = blockContents[124 : 124 + 12].strip(b"\0")
            size = int(rawSize, 8) if rawSize else 0
            blockNumber += ceilDiv(size, 512)
            fileObject.seek(blockNumber * 512)

            # A lot of the special files contain information about the next file, therefore keep do not yield
            # the offset of the next block so that the TAR will not be split between them.
            # K: Identifies the *next* file on the tape as having a long name.
            # L: Identifies the *next* file on the tape as having a long linkname.
            # x: Extended header with meta data for the next file in the archive (POSIX.1-2001)
            # 0: Normal file.
            if typeFlag != b'0':
                skipNextBlocks += 1

    def _processFuture(self, future):
        """Updates progress bar, waits for future and appends the results or even inserts them into the database."""

        # ProgressBar does a similar check like this inside 'update' but doing this outside avoids huge
        # call stacks and also avoids calling tell() on the file object in each loop iteration.
        # I could observe 10% # shorter runtimes because of this with the test file:
        #     tar-with-1000-folders-with-1000-files-0B-files.tar
        if time.time() - self._lastUpdateTime >= 2:
            self._lastUpdateTime = time.time()
            self._updateProgressBar()

        newFileInfos, filesToMountRecursively, _ = future.get()
        self._filesToMountRecursively.extend(filesToMountRecursively)
        self._fileInfos.extend(newFileInfos)
        if len(self._fileInfos) > 1000:
            self._setFileInfos(self._fileInfos)
            self._fileInfos = []

    def _enqueue(self, future):
        """Enqueues future and if a threshold is reached, waits for and pops the oldest future."""

        self._futures.append(future)
        if len(self._futures) > 2 * self._parent.parallelization:
            self._processFuture(self._futures.pop(0))

    def _processParallel(
        self, fileObject: IO[bytes], pathPrefix: str, streamOffset: int, processPool
    ) -> Iterable[Tuple]:
        """
        Iterates over the files inside the TAR to finde good splitting points and then extracts FileInfo tuples
        for partial TARs in parallel using the given processPool.
        """

        self._filesToMountRecursively.clear()
        processedFiles = 0
        tarBlocks: List[int] = []  # Contains offsets for TAR blocks

        offsets = self.findTarFileOffsets(fileObject, self._parent.ignoreZeros)
        while True:
            result = next(offsets, None)
            if result:
                offset, typeFlag = result

                if typeFlag == b'D' and self._parent.isGnuIncremental is None:
                    self._parent.isGnuIncremental = True
                    if self._parent.printDebug >= 1:
                        print("[Warning] A folder metadata entry for GNU incremental archives")
                        print("[Warning] was encountered but this archive was not automatically recognized as such!")
                        print("[Warning] Please call ratarmount with the --gnu-incremental flag if there are problems.")
                        print()

            tarBlocks.append(offset)
            processedFiles += 1

            if len(tarBlocks) >= 10000 or (result is None and len(tarBlocks) > 0):
                if result is None:
                    tarBlocks.append(fileObject.tell())

                startOffset = tarBlocks[0]
                subSize = tarBlocks[-1] - tarBlocks[0]

                tarBlocks = tarBlocks[-1:]

                self._enqueue(
                    processPool.apply_async(
                        self._readTarFiles,
                        (
                            fileObject.name,
                            startOffset,
                            subSize,
                            pathPrefix,
                            streamOffset,
                            self._parent.isGnuIncremental,
                            self._parent.mountRecursively,
                            self._parent.ignoreZeros,
                            self._parent.encoding,
                            self._parent.printDebug,
                        ),
                    )
                )

            if result is None:
                break

        if processedFiles == 0:
            raise RatarmountError("Could not any find TAR blocks!")

        while self._futures:
            self._processFuture(self._futures.pop(0))
        self._setFileInfos(self._fileInfos)
        self._fileInfos = []

        return self._filesToMountRecursively

    def _openTar(self, fileObject: IO[bytes]):
        """
        Opens the fileObject with the appropriate settings using the tarfile module.
        Instead of throwing, an empty iterable might be returned.
        """

        if not self._parent.isTar:
            return []  # Feign an empty TAR file (iterable) if anything goes wrong

        try:
            # r: uses seeks to skip to the next file inside the TAR while r| doesn't do any seeks.
            # r| might be slower but for compressed files we have to go over all the data once anyways.
            # Note that with ignore_zeros = True, no invalid header issues or similar will be raised even for
            # non TAR files!?
            return tarfile.open(
                # fmt:off
                fileobj      = fileObject,
                mode         = 'r|' if self._parent.compression else 'r:',
                ignore_zeros = self._parent.ignoreZeros,
                encoding     = self._parent.encoding,
                # fmt:on
            )
        except tarfile.ReadError:
            pass

        return []

    def _processSerial(self, fileObject: IO[bytes], pathPrefix: str, streamOffset: int) -> Iterable[Tuple]:
        """
        Opens the given fileObject using the tarfile module, iterates over all files converting their metadata to
        FileInfo tuples and inserting those into the databse in a chunked manner using the given _setFileInfos.
        """

        loadedTarFile: Any = self._openTar(fileObject)

        # Iterate over files inside TAR and add them to the database
        fileInfos: List[Tuple] = []
        filesToMountRecursively: List[Tuple] = []

        # thread_time is twice as fast, which can shave off 10% of time in some tests but it is not as "correct"
        # because it does not count the sleep time of the thread, e.g., caused by waiting for I/O or even waiting
        # for work done inside multiprocessing.pool.Pool! This can lead to more than factor 10 distortions and
        # therefore is not suitable. If time.time is indeed an issue, then it should be better to use _processParallel.
        self._lastUpdateTime = time.time()

        try:
            for tarInfo in loadedTarFile:
                loadedTarFile.members = []  # Clear this in order to limit memory usage by tarfile

                # ProgressBar does a similar check like this inside 'update' but doing this outside avoids huge
                # call stacks and also avoids calling tell() on the file object in each loop iteration.
                # I could observe 10% shorter runtimes because of this with the test file:
                #     tar-with-1000-folders-with-1000-files-0B-files.tar
                if time.time() - self._lastUpdateTime >= 2:
                    self._lastUpdateTime = time.time()
                    self._updateProgressBar()

                newFileInfos, mightBeTar, self._parent.isGnuIncremental = _TarFileMetadataReader._processTarInfo(
                    tarInfo,
                    fileObject=fileObject,
                    pathPrefix=pathPrefix,
                    streamOffset=streamOffset,
                    isGnuIncremental=self._parent.isGnuIncremental,
                    mountRecursively=self._parent.mountRecursively,
                    printDebug=self._parent.printDebug,
                )

                if mightBeTar:
                    filesToMountRecursively.extend(newFileInfos)

                fileInfos.extend(newFileInfos)
                if len(fileInfos) > 1000:
                    self._setFileInfos(fileInfos)
                    fileInfos.clear()

        finally:
            self._setFileInfos(fileInfos)

        return filesToMountRecursively

    def process(self, fileObject: IO[bytes], pathPrefix: str, streamOffset: int) -> Iterable[Tuple]:
        """
        Iterates over all files inside the given fileObject TAR and inserts their metadata into the database using
        the given _setFileInfos.
        A list of files which might be of interest for recursive mounting of uncompressed TARs is returned.
        """

        try:
            return self._processSerial(fileObject, pathPrefix, streamOffset)

            # Hidden Feature: Parallelized TAR analysis. It is hidden because it slows things down in certain
            # circumstances. But I did observe a nice speedup for TARs containing only empty files.
            # Probably unchanged for files <= 512B but for anything else it is doubtful whether this parallelization
            # fileCanBeReopenedFromName = (
            #     not self._parent.isFileObject
            #     and hasattr(fileObject, 'name')
            #     and isinstance(fileObject.name, str)
            #     and os.path.isfile(fileObject.name)
            # )
            #
            # # is helpful because of the high amount of random access necessary.
            # # - Parallelizing is only possible for actual files not objects because the file needs to be reopened
            # #   from a different process (not just thread to circumvent the global interpreter lock).
            # # - For compressed files, the bottleneck is the decompression and the necessary seeks for this
            # #   parallelization scheme would slow that down even more.
            # # - If no parallelization is required than fall back to a simple scheme which has been tested for longer
            # #   and should also be smaller because it avoids expensive setup only required for the parallelization.
            # # - Only parallelize on Linux because of multi-file access problems on macOS and Windows.
            # if (
            #     fileCanBeReopenedFromName
            #     and not self._parent.compression
            #     and self._parent.parallelization != 1
            #     and platform.system() == 'Linux'
            #     and streamOffset == 0
            # ):
            #     # Distribute contiguous TAR block ranges to parallel workers
            #     with multiprocessing.pool.Pool(self._parent.parallelization) as pool:
            #         return self._processParallel(fileObject, pathPrefix, streamOffset, pool)
            # else:
            #     return self._processSerial(fileObject, pathPrefix, streamOffset)

        except tarfile.ReadError as e:
            if 'unexpected end of data' in str(e):
                print(
                    "[Warning] The TAR file is incomplete. Ratarmount will work but some files might be cut off. "
                    "If the TAR file size changes, ratarmount will recreate the index during the next mounting."
                )
                if self._parent.printDebug >= 3:
                    traceback.print_exc()

        return []


@dataclass
class SQLiteIndexedTarUserData:
    # fmt: off
    offset       : int
    offsetheader : int
    istar        : bool
    issparse     : bool
    # fmt: on


class SQLiteIndexedTar(MountSource):
    """
    This class reads once through the whole TAR archive and stores TAR file offsets
    for all contained files in an index to support fast seeking to a given file.
    """

    # Version 0.1.0:
    #   - Initial version
    # Version 0.2.0:
    #   - Add sparse support and 'offsetheader' and 'issparse' columns to the SQLite database
    #   - Add TAR file size metadata in order to quickly check whether the TAR changed
    #   - Add 'offsetheader' to the primary key of the 'files' table so that files which were
    #     updated in the TAR can still be accessed if necessary.
    # Version 0.3.0:
    #   - Add arguments influencing the created index to metadata (ignore-zeros, recursive, ...)
    # Version 0.4.0:
    #   - Added 'gzipindexes' table, which may contain multiple blobs in contrast to 'gzipindex' table.
    __version__ = '0.4.0'

    def __init__(
        # fmt: off
        self,
        tarFileName                  : Optional[str]             = None,
        fileObject                   : Optional[IO[bytes]]       = None,
        writeIndex                   : bool                      = False,
        clearIndexCache              : bool                      = False,
        indexFilePath                : Optional[str]             = None,
        indexFolders                 : Optional[List[str]]       = None,
        recursive                    : bool                      = False,
        gzipSeekPointSpacing         : int                       = 4 * 1024 * 1024,
        encoding                     : str                       = tarfile.ENCODING,
        stripRecursiveTarExtension   : bool                      = False,
        ignoreZeros                  : bool                      = False,
        verifyModificationTime       : bool                      = False,
        parallelization              : int                       = 1,
        isGnuIncremental             : Optional[bool]            = None,
        printDebug                   : int                       = 0,
        transformRecursiveMountPoint : Optional[Tuple[str, str]] = None,
        prioritizedBackends          : Optional[List[str]]       = None,
        # pylint: disable=unused-argument
        **kwargs
        # fmt: on
    ) -> None:
        """
        tarFileName : Path to the TAR file to be opened. If not specified, a fileObject must be specified.
                      If only a fileObject is given, the created index can't be cached (efficiently).
        fileObject : A io.IOBase derived object. If not specified, tarFileName will be opened.
                     If it is an instance of IndexedBzip2File, IndexedGzipFile, or IndexedZstdFile, then the offset
                     loading and storing from and to the SQLite database is managed automatically by this class.
        writeIndex : If true, then the sidecar index file will be written to a suitable location.
                     Will be ignored if indexFilePath is ':memory:' or if only fileObject is specified
                     but not tarFileName.
        clearIndexCache : If true, then check all possible index file locations for the given tarFileName/fileObject
                          combination and delete them. This also implicitly forces a recreation of the index.
        indexFilePath : Path to the index file for this TAR archive. This takes precedence over the automatically
                        chosen locations. If it is ':memory:', then the SQLite database will be kept in memory
                        and not stored to the file system at any point.
        indexFolders : Specify one or multiple paths for storing .index.sqlite files. Paths will be tested for
                       suitability in the given order. An empty path will be interpreted as the location in which
                       the TAR resides. This overrides the default index fallback folder in ~/.ratarmount.
        recursive : If true, then TAR files inside this archive will be recursively analyzed and added to the SQLite
                    index. Currently, this recursion can only break the outermost compression layer. I.e., a .tar.bz2
                    file inside a tar.bz2 file can not be mounted recursively.
        gzipSeekPointSpacing : This controls the frequency of gzip decoder seek points, see indexed_gzip documentation.
                               Larger spacings lead to less memory usage but increase the constant seek overhead.
        encoding : Will be forwarded to tarfile. Specifies how filenames inside the TAR are encoded.
        ignoreZeros : Will be forwarded to tarfile. Specifies to not only skip zero blocks but also blocks with
                      invalid data. Setting this to true can lead to some problems but is required to correctly
                      read concatenated tars.
        stripRecursiveTarExtension : If true and if recursive is also true, then a <file>.tar inside the current
                                     tar will be mounted at <file>/ instead of <file>.tar/.
        transformRecursiveMountPoint : If specified, then a <path>.tar inside the current tar will be matched with the
                                       first argument of the tuple and replaced by the second argument. This new
                                       modified path is used as recursive mount point. See also Python's re.sub.
        verifyModificationTime : If true, then the index will be recreated automatically if the TAR archive has a more
                                 recent modification time than the index file.
        isGnuIncremental : If None, then it will be determined automatically. Behavior can be overwritten by setting
                           it to a bool value. If true, then prefixes will be stripped from certain paths encountered
                           with GNU incremental backups.
        kwargs : Unused. Only for compatibility with generic MountSource interface.
        """

        # stores which parent folders were last tried to add to database and therefore do exist
        self.parentFolderCache: List[Tuple[str, str]] = []
        self.sqlConnection: Optional[sqlite3.Connection] = None
        self.indexFilePath = None

        # fmt: off
        self.mountRecursively             = recursive
        self.encoding                     = encoding
        self.stripRecursiveTarExtension   = stripRecursiveTarExtension
        self.transformRecursiveMountPoint = transformRecursiveMountPoint
        self.prioritizedBackends          = prioritizedBackends
        self.ignoreZeros                  = ignoreZeros
        self.verifyModificationTime       = verifyModificationTime
        self.gzipSeekPointSpacing         = gzipSeekPointSpacing
        self.parallelization              = parallelization
        self.printDebug                   = printDebug
        self.isFileObject                 = fileObject is not None
        self.isGnuIncremental             = isGnuIncremental
        self.hasBeenAppendedTo            = False
        self.numberOfMetadataToVerify     = 1000  # shouldn't take more than 1 second according to benchmarks
        # fmt: on

        # Determine an archive file name to show for debug output
        self.tarFileName: str
        if fileObject:
            self.tarFileName = tarFileName if tarFileName else '<file object>'
        else:
            if tarFileName:
                self.tarFileName = os.path.abspath(tarFileName)
            else:
                raise RatarmountError("At least one of tarFileName and fileObject arguments should be set!")

        # If no fileObject given, then self.tarFileName is the path to the archive to open.
        if not fileObject:
            fileObject = open(self.tarFileName, 'rb')
        fileObject.seek(0, io.SEEK_END)
        fileSize = fileObject.tell()
        fileObject.seek(0)  # Even if not interested in the file size, seeking to the start might be useful.

        # rawFileObject : Only set when opening a compressed file and only kept to keep the
        #                 compressed file handle from being closed by the garbage collector.
        # tarFileObject : File object to the uncompressed (or decompressed) TAR file to read actual data out of.
        # compression   : Stores what kind of compression the originally specified TAR file uses.
        # isTar         : Can be false for the degenerated case of only a bz2 or gz file not containing a TAR
        self.tarFileObject, self.rawFileObject, self.compression, self.isTar = SQLiteIndexedTar._openCompressedFile(
            fileObject,
            gzipSeekPointSpacing,
            encoding,
            self.parallelization,
            prioritizedBackends=self.prioritizedBackends,
            printDebug=self.printDebug,
        )
        if not self.isTar and not self.rawFileObject:
            raise RatarmountError("File object (" + str(fileObject) + ") could not be opened as a TAR file!")

        self.fileObjectLock = threading.Lock()

        if self.compression == 'xz':
            try:
                if len(self.tarFileObject.block_boundaries) <= 1 and (fileSize is None or fileSize > 1024 * 1024):
                    print(f"[Warning] The specified file '{self.tarFileName}'")
                    print("[Warning] is compressed using xz but only contains one xz block. This makes it ")
                    print("[Warning] impossible to use true seeking! Please (re)compress your TAR using pixz")
                    print("[Warning] (see https://github.com/vasi/pixz) in order for ratarmount to do be able ")
                    print("[Warning] to do fast seeking to requested files.")
                    print("[Warning] As it is, each file access will decompress the whole TAR from the beginning!")
                    print()
            except Exception:
                pass

        # TODO This does and did not work correctly for recursive TARs because the outermost layer will change None to
        #      a hard value and from then on it would have been fixed to that value even then called inside createIndex.
        if self.isGnuIncremental is None:
            self.isGnuIncremental = self._isGnuIncremental(self.tarFileObject)

        # will be used for storing indexes if current path is read-only
        if self.isFileObject:
            possibleIndexFilePaths = []
            indexPathAsName = None
        else:
            possibleIndexFilePaths = [self.tarFileName + ".index.sqlite"]
            indexPathAsName = self.tarFileName.replace("/", "_") + ".index.sqlite"

        if isinstance(indexFolders, str):
            indexFolders = [indexFolders]

        # A given index file name takes precedence and there should be no implicit fallback
        if indexFilePath:
            if indexFilePath == ':memory:':
                possibleIndexFilePaths = []
            else:
                possibleIndexFilePaths = [os.path.abspath(os.path.expanduser(indexFilePath))]
        elif indexFolders:
            # An empty path is to be interpreted as the default path right besides the TAR
            if '' not in indexFolders:
                possibleIndexFilePaths = []

            if indexPathAsName:
                for folder in indexFolders:
                    if folder:
                        indexPath = os.path.join(folder, indexPathAsName)
                        possibleIndexFilePaths.append(os.path.abspath(os.path.expanduser(indexPath)))
            else:
                writeIndex = False
        elif self.isFileObject:
            writeIndex = False

        if clearIndexCache:
            for indexPath in possibleIndexFilePaths:
                if os.path.isfile(indexPath):
                    os.remove(indexPath)

        # Try to find an already existing index
        for indexPath in possibleIndexFilePaths:
            if self._tryLoadIndex(indexPath):
                self.indexFilePath = indexPath
                break

        if self.indexIsLoaded() and self.sqlConnection:
            try:
                indexVersion = self.sqlConnection.execute(
                    "SELECT major,minor FROM versions WHERE name == 'index';"
                ).fetchone()

                if indexVersion and indexVersion > __version__:
                    print("[Warning] The loaded index was created with a newer version of ratarmount.")
                    print("[Warning] If there are any problems, please update ratarmount or recreate the index")
                    print("[Warning] with this ratarmount version using the --recreate-index option!")
            except Exception:
                pass

            if not self.hasBeenAppendedTo:  # indirectly set by a successful call to _tryLoadIndex
                self._loadOrStoreCompressionOffsets()  # load
                self._reloadIndexReadOnly()
                return

            # TODO Handling appended files to compressed archives would have to account for dropping the offsets,
            #      seeking to the first appended file while not processing any metadata and still showing a progress
            #      bar as well as saving the block offsets out after reading and possibly other things.
            if self.compression:
                # When loading compression offsets, the backends assume they are complete, so we have to clear them.
                self._clearCompressionOffsets()

            pastEndOffset = self._getPastEndOffset(self.sqlConnection)
            if not self.compression and pastEndOffset and self._checkIndexValidity():
                archiveSize = self.tarFileObject.seek(0, io.SEEK_END)

                newShare = (archiveSize - pastEndOffset) / archiveSize
                print(f"Detected TAR being appended to. Will only analyze the newly added {newShare:.2f} % of data.")

                appendedPartAsFile = StenciledFile(
                    fileStencils=[(self.tarFileObject, pastEndOffset, archiveSize - pastEndOffset)]
                )
                self._createIndex(appendedPartAsFile, None, "", pastEndOffset)

                self._loadOrStoreCompressionOffsets()  # store

                self.sqlConnection.execute("DROP TABLE IF EXISTS metadata;")
                self.sqlConnection.execute("DROP TABLE IF EXISTS versions;")
                self._storeMetadata(self.sqlConnection)

                self._reloadIndexReadOnly()
                return

            self.sqlConnection.close()
            self.sqlConnection = None
            print("[Warning] The loaded index does not match the archive. Will recreate it.")

        # Find a suitable (writable) location for the index database
        if writeIndex and indexFilePath != ':memory:':
            for indexPath in possibleIndexFilePaths:
                if self._pathIsWritable(indexPath, printDebug=self.printDebug) and self._pathCanBeUsedForSqlite(
                    indexPath, printDebug=self.printDebug
                ):
                    self.indexFilePath = indexPath
                    break

            if not self.indexFilePath:
                raise InvalidIndexError(
                    "Could not find any existing index or writable location for an index in "
                    + str(possibleIndexFilePaths)
                )

        self._createIndex(self.tarFileObject)
        self._loadOrStoreCompressionOffsets()  # store
        if self.sqlConnection:
            self._storeMetadata(self.sqlConnection)
            self._reloadIndexReadOnly()

        if self.printDebug >= 1 and self.indexFilePath and os.path.isfile(self.indexFilePath):
            # The 0-time is legacy for the automated tests
            # fmt: off
            print("Writing out TAR index to", self.indexFilePath, "took 0s",
                  "and is sized", os.stat( self.indexFilePath ).st_size, "B")
            # fmt: on

    def _isGnuIncremental(self, fileObject: Any) -> bool:
        """Check for GNU incremental backup TARs."""
        oldPos = fileObject.tell()

        t0 = time.time()
        try:
            # For an uncompressed 500MB TAR, this iteration took ~0.7s for 1M files roughly 30x faster than tarfile.
            # But for compressed TARs or for HDDs as opposed to SSDs, this might be much slower.
            nMaxToTry = 1000 if self.isFileObject or self.compression else 10000
            for _, typeFlag in _TarFileMetadataReader.findTarFileOffsets(fileObject, self.ignoreZeros):
                # It seems to be possible to create mixtures of incremental archives and normal contents,
                # therefore do not check that all files must have the mtime prefix.
                if typeFlag == b'D':
                    if self.printDebug >= 1:
                        print("[Info] Detected GNU incremental TAR.")
                    return True

                nMaxToTry -= 1
                if nMaxToTry <= 0 or time.time() - t0 > 3:
                    break

        except Exception as exception:
            if self.printDebug >= 2:
                print("[Info] TAR was not recognized as GNU incremental TAR because of exception", exception)
            if self.printDebug >= 3:
                traceback.print_exc()
        finally:
            fileObject.seek(oldPos)

        return False

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self.sqlConnection:
            self.sqlConnection.commit()
            self.sqlConnection.close()

        if self.tarFileObject:
            self.tarFileObject.close()

        if self.rawFileObject:
            self.tarFileObject.close()

    def _storeMetadata(self, connection: sqlite3.Connection) -> None:
        self._storeVersionsMetadata(connection, printDebug=self.printDebug)

        metadataTable = """
            /* empty table whose sole existence specifies that we finished iterating the tar */
            CREATE TABLE "metadata" (
                "key"      VARCHAR(65535) NOT NULL, /* e.g. "tarsize" */
                "value"    VARCHAR(65535) NOT NULL  /* e.g. size in bytes as integer */
            );
        """

        connection.executescript(metadataTable)

        # All of these require the generic "metadata" table.
        if not self.isFileObject:
            self._storeTarMetadata(connection, self.tarFileName, printDebug=self.printDebug)
        self._storeArgumentsMetadata(connection)
        connection.commit()

    @staticmethod
    def _storeVersionsMetadata(connection: sqlite3.Connection, printDebug: int = 0) -> None:
        versionsTable = """
            /* This table's sole existence specifies that we finished iterating the tar for older ratarmount versions */
            CREATE TABLE "versions" (
                "name"     VARCHAR(65535) NOT NULL, /* which component the version belongs to */
                "version"  VARCHAR(65535) NOT NULL, /* free form version string */
                /* Semantic Versioning 2.0.0 (semver.org) parts if they can be specified:
                 *   MAJOR version when you make incompatible API changes,
                 *   MINOR version when you add functionality in a backwards compatible manner, and
                 *   PATCH version when you make backwards compatible bug fixes. */
                "major"    INTEGER,
                "minor"    INTEGER,
                "patch"    INTEGER
            );
        """
        try:
            connection.executescript(versionsTable)
        except Exception as exception:
            print("[Warning] There was an error when adding metadata information. Index loading might not work.")
            if printDebug >= 2:
                print(exception)
            if printDebug >= 3:
                traceback.print_exc()

        try:

            def makeVersionRow(
                versionName: str, version: str
            ) -> Tuple[str, str, Optional[str], Optional[str], Optional[str]]:
                versionNumbers = [re.sub('[^0-9]', '', x) for x in version.split('.')]
                return (
                    versionName,
                    version,
                    versionNumbers[0] if len(versionNumbers) > 0 else None,
                    versionNumbers[1] if len(versionNumbers) > 1 else None,
                    versionNumbers[2] if len(versionNumbers) > 2 else None,
                )

            versions = [
                makeVersionRow('ratarmount', __version__),
                makeVersionRow('index', SQLiteIndexedTar.__version__),
            ]

            for moduleName in set(
                module.name
                for _, info in TAR_COMPRESSION_FORMATS.items()
                for module in info.modules
                if module.name in sys.modules
            ):
                moduleVersion = findModuleVersion(sys.modules[moduleName])
                if moduleVersion:
                    versions += [makeVersionRow(moduleName, moduleVersion)]

            connection.executemany('INSERT OR REPLACE INTO "versions" VALUES (?,?,?,?,?)', versions)
        except Exception as exception:
            print("[Warning] There was an error when adding version information.")
            if printDebug >= 2:
                print(exception)
            if printDebug >= 3:
                traceback.print_exc()

    @staticmethod
    def _storeTarMetadata(connection: sqlite3.Connection, tarPath: AnyStr, printDebug: int = 0) -> None:
        """Adds some consistency meta information to recognize the need to update the cached TAR index"""
        try:
            tarStats = os.stat(tarPath)
            serializedTarStats = json.dumps(
                {attr: getattr(tarStats, attr) for attr in dir(tarStats) if attr.startswith('st_')}
            )
            connection.execute('INSERT INTO "metadata" VALUES (?,?)', ("tarstats", serializedTarStats))
        except Exception as exception:
            print("[Warning] There was an error when adding file metadata.")
            print("[Warning] Automatic detection of changed TAR files during index loading might not work.")
            if printDebug >= 2:
                print(exception)
            if printDebug >= 3:
                traceback.print_exc()

    def _storeArgumentsMetadata(self, connection: sqlite3.Connection) -> None:
        argumentsToSave = [
            'mountRecursively',
            'gzipSeekPointSpacing',
            'encoding',
            'stripRecursiveTarExtension',
            'transformRecursiveMountPoint',
            'ignoreZeros',
        ]

        argumentsMetadata = json.dumps({argument: getattr(self, argument) for argument in argumentsToSave})

        try:
            connection.execute('INSERT INTO "metadata" VALUES (?,?)', ("arguments", argumentsMetadata))
        except Exception as exception:
            if self.printDebug >= 2:
                print(exception)
            print("[Warning] There was an error when adding argument metadata.")
            print("[Warning] Automatic detection of changed arguments files during index loading might not work.")

    @staticmethod
    def _pathIsWritable(path: AnyStr, printDebug: int = 0) -> bool:
        try:
            folder = os.path.dirname(path)
            if folder:
                os.makedirs(folder, exist_ok=True)

            with open(path, 'wb') as file:
                file.write(b'\0' * 1024 * 1024)
            os.remove(path)

            return True

        except PermissionError:
            if printDebug >= 2:
                traceback.print_exc()
                print("Could not create file:", path)

        except IOError:
            if printDebug >= 2:
                traceback.print_exc()
                print("Could not create file:", path)

        return False

    @staticmethod
    def _pathCanBeUsedForSqlite(path: AnyStr, printDebug: int = 0) -> bool:
        fileExisted = os.path.isfile(path)
        try:
            folder = os.path.dirname(path)
            if folder:
                os.makedirs(folder, exist_ok=True)

            connection = SQLiteIndexedTar._openSqlDb(path)
            connection.executescript('CREATE TABLE "files" ( "path" VARCHAR(65535) NOT NULL );')
            connection.commit()
            connection.close()
            return True
        except sqlite3.OperationalError:
            if printDebug >= 2:
                traceback.print_exc()
                print("Could not create SQLite database at:", path)
        finally:
            if not fileExisted and os.path.isfile(path):
                SQLiteIndexedTar._uncheckedRemove(path)

        return False

    @staticmethod
    def _openSqlDb(path: AnyStr, **kwargs) -> sqlite3.Connection:
        sqlConnection = sqlite3.connect(path, **kwargs)
        sqlConnection.row_factory = sqlite3.Row
        sqlConnection.executescript(
            # Locking mode exclusive leads to a measurable speedup. E.g., find on 2k recursive files tar
            # improves from ~1s to ~0.4s!
            # https://blog.devart.com/increasing-sqlite-performance.html
            """
            PRAGMA LOCKING_MODE = EXCLUSIVE;
            PRAGMA TEMP_STORE = MEMORY;
            PRAGMA JOURNAL_MODE = OFF;
            PRAGMA SYNCHRONOUS = OFF;
            """
        )
        return sqlConnection

    CREATE_FILES_TABLE = """
        CREATE TABLE "files" (
            "path"          VARCHAR(65535) NOT NULL,  /* path with leading and without trailing slash */
            "name"          VARCHAR(65535) NOT NULL,
            "offsetheader"  INTEGER,  /* seek offset from TAR file where the TAR metadata for this file resides */
            "offset"        INTEGER,  /* seek offset from TAR file where these file's contents resides */
            "size"          INTEGER,
            "mtime"         REAL,
            "mode"          INTEGER,
            "type"          INTEGER,
            "linkname"      VARCHAR(65535),
            "uid"           INTEGER,
            "gid"           INTEGER,
            /* True for valid TAR files. Internally used to determine where to mount recursive TAR files. */
            "istar"         BOOL   ,
            "issparse"      BOOL   ,  /* for sparse files the file size refers to the expanded size! */
            /* See SQL benchmarks for decision on the primary key.
             * See also https://www.sqlite.org/optoverview.html
             * (path,name) tuples might appear multiple times in a TAR if it got updated.
             * In order to also be able to show older versions, we need to add
             * the offsetheader column to the primary key. */
            PRIMARY KEY (path,name,offsetheader)
        );"""

    CREATE_FILESTMP_TABLE = """
        /* "A table created using CREATE TABLE AS has no PRIMARY KEY and no constraints of any kind"
         * Therefore, it will not be sorted and inserting will be faster! */
        CREATE TABLE "filestmp" AS SELECT * FROM "files" WHERE 0;"""

    CREATE_PARENT_FOLDERS_TABLE = """
        CREATE TABLE "parentfolders" (
            "path"          VARCHAR(65535) NOT NULL,
            "name"          VARCHAR(65535) NOT NULL,
            "offsetheader"  INTEGER,
            "offset"        INTEGER,
            PRIMARY KEY (path,name)
            UNIQUE (path,name)
        );"""

    @staticmethod
    def _getSqliteTables(connection: sqlite3.Connection):
        return [x[0] for x in connection.execute('SELECT name FROM sqlite_master WHERE type="table"')]

    @staticmethod
    def _initializeSqlDb(indexFilePath: Optional[str], printDebug: int = 0) -> sqlite3.Connection:
        if printDebug >= 1:
            print("Creating new SQLite index database at", indexFilePath if indexFilePath else ':memory:')

        sqlConnection = SQLiteIndexedTar._openSqlDb(indexFilePath if indexFilePath else ':memory:')
        tables = SQLiteIndexedTar._getSqliteTables(sqlConnection)
        if {"files", "filestmp", "parentfolders"}.intersection(tables):
            raise InvalidIndexError(
                f"The index file {indexFilePath} already seems to contain a table. Please specify --recreate-index."
            )
        sqlConnection.executescript(SQLiteIndexedTar.CREATE_FILES_TABLE)
        return sqlConnection

    def _reloadIndexReadOnly(self):
        if not self.indexFilePath or self.indexFilePath == ':memory:' or not self.sqlConnection:
            return

        self.sqlConnection.commit()
        self.sqlConnection.close()

        uriPath = urllib.parse.quote(self.indexFilePath)
        # check_same_thread=False can be used because it is read-only anyway and it allows to enable FUSE multithreading
        self.sqlConnection = SQLiteIndexedTar._openSqlDb(f"file:{uriPath}?mode=ro", uri=True, check_same_thread=False)

    def _updateProgressBar(self, progressBar, fileobj: Any) -> None:
        if not progressBar:
            return

        try:
            if hasattr(fileobj, 'tell_compressed') and self.compression == 'bz2':
                # Note that because bz2 works on a bitstream the tell_compressed returns the offset in bits
                progressBar.update(fileobj.tell_compressed() // 8)
            elif hasattr(fileobj, 'tell_compressed'):
                progressBar.update(fileobj.tell_compressed())
            elif hasattr(fileobj, 'fileobj') and callable(fileobj.fileobj):
                progressBar.update(fileobj.fileobj().tell())
            elif isinstance(fileobj, ParallelXZReader):
                progressBar.update(fileobj.tell())
            elif self.rawFileObject and hasattr(self.rawFileObject, 'tell'):
                progressBar.update(self.rawFileObject.tell())
            else:
                progressBar.update(fileobj.tell())
        except Exception as exception:
            if self.printDebug >= 1:
                print("An exception occured when trying to update the progress bar:", exception)
            if self.printDebug >= 3:
                traceback.print_exc()

    def _createIndex(
        self,
        # fmt: off
        fileObject  : IO[bytes],
        progressBar : Optional[Any] = None,
        pathPrefix  : str = '',
        streamOffset: int = 0
        # fmt: on
    ) -> None:
        if self.printDebug >= 1:
            print(f"Creating offset dictionary for {self.tarFileName} ...")
        t0 = timer()

        # 1. If no SQL connection was given (by recursive call), open a new database file
        cleanupTemporaryTables = False
        if not self.indexIsLoaded() or not self.sqlConnection:
            cleanupTemporaryTables = True
            self.sqlConnection = self._initializeSqlDb(self.indexFilePath, printDebug=self.printDebug)

        tables = SQLiteIndexedTar._getSqliteTables(self.sqlConnection)
        if "filestmp" not in tables and "parentfolders" not in tables:
            self.sqlConnection.execute(SQLiteIndexedTar.CREATE_FILESTMP_TABLE)
            self.sqlConnection.execute(SQLiteIndexedTar.CREATE_PARENT_FOLDERS_TABLE)
            cleanupTemporaryTables = True
        elif "filestmp" not in tables or "parentfolders" not in tables:
            raise InvalidIndexError(
                "The index file is in an invalid state because it contains some tables and misses others. "
                "Please specify --recreate-index to overwrite the existing index."
            )

        if progressBar is None:
            fileSize = None
            try:
                fileSize = os.fstat(fileObject.fileno()).st_size
            except io.UnsupportedOperation:
                pass

            if fileSize is None and isinstance(fileObject, ParallelXZReader):
                oldOffset = fileObject.tell()
                try:
                    # This is O(1) because xz stores the block information easily accessible
                    fileSize = fileObject.seek(0, io.SEEK_END)
                finally:
                    fileObject.seek(oldOffset)

            if fileSize is not None:
                progressBar = ProgressBar(fileSize)
            elif self.printDebug >= 2:
                print("[Info] Could not create a progress bar because the file size could not be queried.")

        metadataReader = _TarFileMetadataReader(
            self, self._setFileInfos, lambda: self._updateProgressBar(progressBar, fileObject)
        )
        filesToMountRecursively = metadataReader.process(fileObject, pathPrefix, streamOffset)

        # 4. Open contained TARs for recursive mounting
        oldPos = fileObject.tell()
        oldPrintName = self.tarFileName
        for fileInfo in filesToMountRecursively:
            modifiedFolder = fileInfo[0]
            modifiedName = fileInfo[1]

            # Strip file extension for mount point if so configured
            tarExtension = '.tar'
            if (
                self.stripRecursiveTarExtension
                and len(tarExtension) > 0
                and modifiedName.lower().endswith(tarExtension.lower())
            ):
                modifiedName = modifiedName[: -len(tarExtension)]

            # Apply regex transformation to get mount point
            pattern = self.transformRecursiveMountPoint
            modifiedPath = '/' + ('/'.join([modifiedFolder, modifiedName])).lstrip('/')
            if isinstance(pattern, (tuple, list)) and len(pattern) == 2:
                modifiedPath = '/' + re.sub(pattern[0], pattern[1], modifiedPath).lstrip('/')
                modifiedFolder, modifiedName = modifiedPath.rsplit('/', 1)

            # Temporarily change tarFileName for the info output of the recursive call
            self.tarFileName = os.path.join(fileInfo[0], fileInfo[1])

            # StenciledFile's tell returns the offset inside the file chunk instead of the global one,
            # so we have to always communicate the offset of this chunk to the recursive call no matter
            # whether tarfile has streaming access or seeking access!
            globalOffset = fileInfo[3]
            size = fileInfo[4]
            # fileObject already effectively applies streamOffset, so we can't use the globalOffset here!
            # For all supported cases, it should be fine to directly use self.tarFileObject instead of fileObject.
            # This would also save some indirections to speed up accesses.
            tarFileObject = StenciledFile([(self.tarFileObject, globalOffset, size)])

            isTar = False
            try:
                # Do not use os.path.join here because the leading / might be missing.
                # This should instead be seen as the reverse operation of the rsplit further above.
                self._createIndex(tarFileObject, progressBar, modifiedPath, globalOffset)
                isTar = True
            except tarfile.ReadError:
                pass
            finally:
                del tarFileObject

            if isTar:
                modifiedFileInfo = list(fileInfo)

                # if the TAR file contents could be read, we need to adjust the actual
                # TAR file's metadata to be a directory instead of a file
                mode = modifiedFileInfo[6]
                mode = (
                    (mode & 0o777)
                    | stat.S_IFDIR
                    | (stat.S_IXUSR if mode & stat.S_IRUSR != 0 else 0)
                    | (stat.S_IXGRP if mode & stat.S_IRGRP != 0 else 0)
                    | (stat.S_IXOTH if mode & stat.S_IROTH != 0 else 0)
                )

                if modifiedFolder != modifiedFileInfo[0] or modifiedName != modifiedFileInfo[1]:
                    modifiedFileInfo[0] = modifiedFolder
                    modifiedFileInfo[1] = modifiedName
                else:
                    # Increment offset and offsetheader such that the new folder is seen as a more recent version
                    # of the already existing file path for the archive if it has the same path. Else, it would
                    # be undetermined which version is to be counted as more recent when using ORDER BY offsetheader.
                    # Note that offset and offsetheader contain a lot of redundant bits anyway because they are known
                    # to be 0 modulo 512, so the original offsets can be reconstructed even after adding 1.
                    modifiedFileInfo[2] = modifiedFileInfo[2] + 1
                    modifiedFileInfo[3] = modifiedFileInfo[3] + 1
                modifiedFileInfo[6] = mode
                modifiedFileInfo[11] = isTar

                self._setFileInfo(tuple(modifiedFileInfo))

                # Update isTar to True for the tar
                modifiedFileInfo = list(fileInfo)
                modifiedFileInfo[11] = isTar
                self._setFileInfo(tuple(modifiedFileInfo))

        fileObject.seek(oldPos)
        self.tarFileName = oldPrintName

        # If no file is in the TAR, then it most likely indicates a possibly compressed non TAR file.
        # In that case add that itself to the file index. This will be ignored when called recursively
        # because the table will at least contain the recursive file to mount itself, i.e., fileCount > 0
        fileCount = self.sqlConnection.execute('SELECT COUNT(*) FROM "files";').fetchone()[0]
        if fileCount == 0:
            if self.printDebug >= 3:
                print(f"Did not find any file in the given TAR: {self.tarFileName}. Assuming a compressed file.")

            tarInfo: Optional[Any] = None
            try:
                tarInfo = os.fstat(fileObject.fileno())
            except io.UnsupportedOperation:
                # If fileObject doesn't have a fileno, we set tarInfo to None
                # and set the relevant statistics (such as st_mtime) to sensible defaults.
                tarInfo = None

            fname = os.path.basename(self.tarFileName)
            for suffix in ['.gz', '.bz2', '.bzip2', '.gzip', '.xz', '.zst', '.zstd']:
                if fname.lower().endswith(suffix) and len(fname) > len(suffix):
                    fname = fname[: -len(suffix)]
                    break

            # Try to get original file name from gzip
            mtime = 0
            if self.rawFileObject:
                oldPos = self.rawFileObject.tell()
                self.rawFileObject.seek(0)
                try:
                    info = getGzipInfo(self.rawFileObject)
                    if info:
                        fname, mtime = info
                except Exception:
                    if self.printDebug >= 2:
                        print("[Info] Could not determine an original gzip file name probably because it is not a gzip")
                    if self.printDebug >= 3:
                        traceback.print_exc()
                finally:
                    # TODO Why does tell return negative numbers!? Problem with indexed_gzip?
                    self.rawFileObject.seek(max(0, oldPos))

            # If the file object is actually an IndexedBzip2File or such, we can't directly use the file size
            # from os.stat and instead have to gather it from seek. Unfortunately, indexed_gzip does not support
            # io.SEEK_END even though it could as it has the index ...
            while fileObject.read(1024 * 1024):
                self._updateProgressBar(progressBar, fileObject)
            fileSize = fileObject.tell()

            mode = 0o777 | stat.S_IFREG  # default mode

            # fmt: off
            fileInfo = (
                ""                                    ,  # 0 path
                fname                                 ,  # 1
                None                                  ,  # 2 header offset
                0                                     ,  # 3 data offset
                fileSize                              ,  # 4
                tarInfo.st_mtime if tarInfo else mtime,  # 5
                tarInfo.st_mode if tarInfo else mode  ,  # 6
                None                                  ,  # 7 TAR file type. Currently unused. Overlaps with mode
                None                                  ,  # 8 linkname
                tarInfo.st_uid if tarInfo else 0      ,  # 9
                tarInfo.st_gid if tarInfo else 0      ,  # 10
                False              ,  # 11 isTar
                False              ,  # 12 isSparse, don't care if it is actually sparse or not because it is not in TAR
            )
            # fmt: on
            self._setFileInfo(fileInfo)

        # All the code below is for database finalizing which should not be done in a recursive call of createIndex!
        if not cleanupTemporaryTables:
            return

        # 5. Resort by (path,name). This one-time resort is faster than resorting on each INSERT (cache spill)
        if self.printDebug >= 2:
            print("Resorting files by path ...")

        try:
            queriedLibSqliteVersion = sqlite3.connect(":memory:").execute("select sqlite_version();").fetchone()
            libSqliteVersion = tuple(int(x) for x in queriedLibSqliteVersion[0].split('.'))
        except Exception:
            libSqliteVersion = (0, 0, 0)

        searchByTuple = """(path,name) NOT IN ( SELECT path,name"""
        searchByConcat = """path || "/" || name NOT IN ( SELECT path || "/" || name"""

        cleanupDatabase = f"""
            INSERT OR REPLACE INTO "files" SELECT * FROM "filestmp" ORDER BY "path","name",rowid;
            DROP TABLE "filestmp";
            INSERT OR IGNORE INTO "files"
                /* path name offsetheader offset size mtime mode type linkname uid gid istar issparse */
                SELECT path,name,offsetheader,offset,0,0,{int(0o555 | stat.S_IFDIR)},{int(tarfile.DIRTYPE)},"",0,0,0,0
                FROM "parentfolders"
                WHERE {searchByTuple if libSqliteVersion >= (3,22,0) else searchByConcat}
                    FROM "files" WHERE mode & (1 << 14) != 0
                )
                ORDER BY "path","name";
            DROP TABLE "parentfolders";
            PRAGMA optimize;
        """
        self.sqlConnection.executescript(cleanupDatabase)

        t1 = timer()
        if self.printDebug >= 1:
            print(f"Creating offset dictionary for {self.tarFileName} took {t1 - t0:.2f}s")

    @overrides(MountSource)
    def isImmutable(self) -> bool:
        return True

    @staticmethod
    def _rowToFileInfo(row: Dict[str, Any]) -> FileInfo:
        userData = SQLiteIndexedTarUserData(
            # fmt: off
            offset       = row['offset'],
            offsetheader = row['offsetheader'] if 'offsetheader' in row.keys() else 0,
            istar        = row['istar'],
            issparse     = row['issparse'] if 'issparse' in row.keys() else False,
            # fmt: on
        )

        fileInfo = FileInfo(
            # fmt: off
            size     = row['size'],
            mtime    = row['mtime'],
            mode     = row['mode'],
            linkname = row['linkname'],
            uid      = row['uid'],
            gid      = row['gid'],
            userdata = [userData],
            # fmt: on
        )

        return fileInfo

    @overrides(MountSource)
    def getFileInfo(self, path: str, fileVersion: int = 0) -> Optional[FileInfo]:
        fileInfo = self._getFileInfo(path, fileVersion=fileVersion)

        if fileInfo is None:
            return None

        assert isinstance(fileInfo, FileInfo)
        return fileInfo

    def _getFileInfo(
        self,
        # fmt: off
        fullPath     : str,
        listDir      : bool = False,
        listVersions : bool = False,
        fileVersion  : int  = 0
        # fmt: on
    ) -> Optional[Union[FileInfo, Dict[str, FileInfo]]]:
        """
        This is the heart of this class' public interface!

        path    : full path to file where '/' denotes TAR's root, e.g., '/', or '/foo'
        listDir : if True, return a dictionary for the given directory path: { fileName : FileInfo, ... }
                  if False, return simple FileInfo to given path (directory or file)
        fileVersion : If the TAR contains the same file path multiple times, by default only the last one is shown.
                      But with this argument other versions can be queried. Version 1 is the oldest one.
                      Version 0 translates to the most recent one for compatibility with tar --occurrence=<number>.
                      Version -1 translates to the second most recent, and so on.
                      For listDir=True, the file version makes no sense and is ignored!
                      So, even if a folder was overwritten by a file, which is already not well supported by tar,
                      then listDir for that path will still list all contents of the overwritten folder or folders,
                      no matter the specified version. The file system layer has to take care that a directory
                      listing is not even requested in the first place if it is not a directory.
                      FUSE already does this by calling getattr for all parent folders in the specified path first.

        If path does not exist, always return None

        If listVersions is true, then return metadata for all versions of a file possibly appearing more than once
        in the TAR as a directory dictionary. listDir will then be ignored!
        """
        # TODO cache last listDir as most often a stat over all entries will soon follow

        if not isinstance(fileVersion, int):
            raise RatarmountError("The specified file version must be an integer!")
        if not self.sqlConnection:
            raise IndexNotOpenError("This method can not be called without an opened index database!")

        # also strips trailing '/' except for a single '/' and leading '/'
        fullPath = '/' + os.path.normpath(fullPath).lstrip('/')

        if listVersions:
            path, name = fullPath.rsplit('/', 1)
            rows = self.sqlConnection.execute(
                'SELECT * FROM "files" WHERE "path" == (?) AND "name" == (?) ORDER BY "offsetheader" ASC', (path, name)
            )
            result = {str(version + 1): self._rowToFileInfo(row) for version, row in enumerate(rows)}
            return result

        if listDir:
            # For listing directory entries the file version can't be applied meaningfully at this abstraction layer.
            # E.g., should it affect the file version of the directory to list, or should it work on the listed files
            # instead and if so how exactly if there aren't the same versions for all files available, ...?
            # Or, are folders assumed to be overwritten by a new folder entry in a TAR or should they be union mounted?
            # If they should be union mounted, like is the case now, then the folder version only makes sense for
            # its attributes.
            rows = self.sqlConnection.execute('SELECT * FROM "files" WHERE "path" == (?)', (fullPath.rstrip('/'),))
            directory = {}
            gotResults = False
            for row in rows:
                gotResults = True
                if row['name']:
                    directory[row['name']] = self._rowToFileInfo(row)
            return directory if gotResults else None

        path, name = fullPath.rsplit('/', 1)
        row = self.sqlConnection.execute(
            f"""
            SELECT * FROM "files"
            WHERE "path" == (?) AND "name" == (?)
            ORDER BY "offsetheader" {'DESC' if fileVersion is None or fileVersion <= 0 else 'ASC'}
            LIMIT 1 OFFSET (?);
            """,
            (path, name, 0 if fileVersion is None else fileVersion - 1 if fileVersion > 0 else -fileVersion),
        ).fetchone()
        return self._rowToFileInfo(row) if row else None

    def isDir(self, path: str) -> bool:
        """Return true if path exists and is a folder."""
        return self.listDir(path) is not None

    @overrides(MountSource)
    def listDir(self, path: str) -> Optional[Union[Iterable[str], Dict[str, FileInfo]]]:
        """
        Usability wrapper for getFileInfo(listDir=True) with FileInfo stripped if you are sure you don't need it.
        """
        result = self._getFileInfo(path, listDir=True)
        if isinstance(result, dict):
            return result
        return None

    @overrides(MountSource)
    def fileVersions(self, path: str) -> int:
        """
        Usability wrapper for getFileInfo(listVersions=True) with FileInfo stripped if you are sure you don't need it.
        """
        fileVersions = self._getFileInfo(path, listVersions=True)
        return len(fileVersions) if isinstance(fileVersions, dict) else 0

    @overrides(MountSource)
    def open(self, fileInfo: FileInfo) -> IO[bytes]:
        assert fileInfo.userdata
        tarFileInfo = fileInfo.userdata[-1]
        assert isinstance(tarFileInfo, SQLiteIndexedTarUserData)

        # This is not strictly necessary but it saves two file object layers and therefore might be more performant.
        # Furthermore, non-sparse files should be the much more likely case anyway.
        if not tarFileInfo.issparse:
            return cast(
                IO[bytes], StenciledFile([(self.tarFileObject, tarFileInfo.offset, fileInfo.size)], self.fileObjectLock)
            )

        # The TAR file format is very simple. It's just a concatenation of TAR blocks. There is not even a
        # global header, only the TAR block headers. That's why we can simply cut out the TAR block for
        # the sparse file using StenciledFile and then use tarfile on it to expand the sparse file correctly.
        tarBlockSize = tarFileInfo.offset - tarFileInfo.offsetheader + fileInfo.size

        tarSubFile = StenciledFile([(self.tarFileObject, tarFileInfo.offsetheader, tarBlockSize)], self.fileObjectLock)
        # TODO It might be better to somehow call close on tarFile but the question is where and how.
        #      It would have to be appended to the __exit__ method of fileObject like if being decorated.
        #      For now this seems to work either because fileObject does not require tarFile to exist
        #      or because tarFile is simply not closed correctly here, I'm not sure.
        #      Sparse files are kinda edge-cases anyway, so it isn't high priority as long as the tests work.
        tarFile = tarfile.open(fileobj=cast(IO[bytes], tarSubFile), mode='r:', encoding=self.encoding)
        fileObject = tarFile.extractfile(next(iter(tarFile)))
        if not fileObject:
            raise CompressionError("tarfile.extractfile returned nothing!")

        return fileObject

    @overrides(MountSource)
    def read(self, fileInfo: FileInfo, size: int, offset: int) -> bytes:
        assert fileInfo.userdata
        tarFileInfo = fileInfo.userdata[-1]
        assert isinstance(tarFileInfo, SQLiteIndexedTarUserData)

        if tarFileInfo.issparse:
            with self.open(fileInfo) as file:
                file.seek(offset, os.SEEK_SET)
                return file.read(size)

        # For non-sparse files, we can simply seek to the offset and read from it.
        self.tarFileObject.seek(tarFileInfo.offset + offset, os.SEEK_SET)
        return self.tarFileObject.read(size)

    def _tryAddParentFolders(self, path: str, offsetheader: int, offset: int) -> None:
        # Add parent folders if they do not exist.
        # E.g.: path = '/a/b/c' -> paths = [('', 'a'), ('/a', 'b'), ('/a/b', 'c')]
        # Without the parentFolderCache, the additional INSERT statements increase the creation time
        # from 8.5s to 12s, so almost 50% slowdown for the 8MiB test TAR!
        pathParts = path.split("/")
        paths = [
            p
            # fmt: off
            for p in (
                ( "/".join( pathParts[:i] ), pathParts[i] )
                for i in range( 1, len( pathParts ) )
            )
            # fmt: on
            if p not in self.parentFolderCache
        ]
        if not paths:
            return

        self.parentFolderCache += paths
        # Assuming files in the TAR are sorted by hierarchy, the maximum parent folder cache size
        # gives the maximum cacheable file nesting depth. High numbers lead to higher memory usage and lookup times.
        if len(self.parentFolderCache) > 16:
            self.parentFolderCache = self.parentFolderCache[-8:]

        if not self.sqlConnection:
            raise IndexNotOpenError("This method can not be called without an opened index database!")

        # TODO This method is still not perfect but I do not know how to perfect it without loosing significant
        #      performance. Currently, adding implicit folders will fail when a file is overwritten implicitly with
        #      a folder and then overwritten by a file and then again overwritten by a folder. Because the parent
        #      folder was already added implicitly the first time, the second time will be skipped.
        #      To solve this, I would have to add all parent folders for all files, which might easily explode
        #      the temporary database and the indexing performance by the folder depth.
        #      Also, I do not want to add versions for a parent folder for each implicitly added parent folder for
        #      each file, so I would have to sort out those in a post-processing step. E.g., sort by offsetheader
        #      and then clean out successive implicitly added folders as long as there is no file of the same name
        #      in between.
        #      The unmentioned alternative would be to lookup paths with LIKE but that is just madness because it
        #      will have a worse complexity of O(N) instead of O(log(N)).
        self.sqlConnection.executemany(
            'INSERT OR IGNORE INTO "parentfolders" VALUES (?,?,?,?)',
            [(p[0], p[1], offsetheader, offset) for p in paths],
        )

    def _setFileInfos(self, rows: List[Tuple]) -> None:
        if not self.sqlConnection:
            raise IndexNotOpenError("This method can not be called without an opened index database!")
        if not rows:
            return

        try:
            self.sqlConnection.executemany(
                'INSERT OR REPLACE INTO "files" VALUES (' + ','.join('?' * len(rows[0])) + ');', rows
            )
        except UnicodeEncodeError:
            # Fall back to separately inserting each row to find those in need of string cleaning.
            for row in rows:
                self._setFileInfo(row)
            return

        for row in rows:
            self._tryAddParentFolders(row[0], row[2], row[3])

    @staticmethod
    def _escapeInvalidCharacters(toEscape: str, encoding: str):
        try:
            toEscape.encode()
            return toEscape
        except UnicodeEncodeError:
            return toEscape.encode(encoding, 'surrogateescape').decode(encoding, 'backslashreplace')

    def _setFileInfo(self, row: tuple) -> None:
        if not self.sqlConnection:
            raise IndexNotOpenError("This method can not be called without an opened index database!")

        try:
            self.sqlConnection.execute('INSERT OR REPLACE INTO "files" VALUES (' + ','.join('?' * len(row)) + ');', row)
        except UnicodeEncodeError:
            print("[Warning] Problem caused by file name encoding when trying to insert this row:", row)
            print("[Warning] The file name will now be stored with the bad character being escaped")
            print("[Warning] instead of being correctly interpreted.")
            print("[Warning] Please specify a suitable file name encoding using, e.g., --encoding iso-8859-1!")
            print("[Warning] A list of possible encodings can be found here:")
            print("[Warning] https://docs.python.org/3/library/codecs.html#standard-encodings")

            checkedRow = []
            for x in list(row):  # check strings
                if isinstance(x, str):
                    checkedRow += [self._escapeInvalidCharacters(x, self.encoding)]
                else:
                    checkedRow += [x]

            self.sqlConnection.execute(
                'INSERT OR REPLACE INTO "files" VALUES (' + ','.join('?' * len(row)) + ');', tuple(checkedRow)
            )
            print("[Warning] The escaped inserted row is now:", row)
            print()

            self._tryAddParentFolders(self._escapeInvalidCharacters(row[0], self.encoding), row[2], row[3])
            return

        self._tryAddParentFolders(row[0], row[2], row[3])

    def indexIsLoaded(self) -> bool:
        """Returns true if the SQLite database has been opened for reading and a "files" table exists."""
        if not self.sqlConnection:
            return False

        try:
            self.sqlConnection.execute('SELECT * FROM "files" WHERE 0 == 1;')
        except sqlite3.OperationalError:
            self.sqlConnection = None
            return False

        return True

    @staticmethod
    def _getPastEndOffset(sqlConnection: sqlite3.Connection) -> Optional[int]:
        """
        Returns None if it cannot determine where the archive should end. Currently, because of implementation
        limitations, this may happen if the last entry in the archive is a sparse file.
        """
        # TODO Make it work with sparse files by analyzing those sparse blocks manually or maybe get tarfile to do it

        # Note that we cannot use the recorded archive file size to determine from which we need to resume
        # reading because it is not specified how many zero-byte blocks there may be at the end:
        # > At the end of the archive file there shall be two 512-byte blocks filled with binary zeros,
        # > interpreted as an end-of-archive indicator.
        # For example, GNU tar rounds up to 10 KiB for very small archives but will (have to) append further
        # files right after the the last non-zero block, which might be at offset 512 for empty files.
        # > The user can specify a blocking factor, which is the number of blocks per record.
        # > The default is 20, producing 10 KiB records.
        pastEndOffset, isSparse = sqlConnection.execute(
            "SELECT offset + size, issparse FROM files ORDER BY offset DESC LIMIT 1"
        ).fetchone()

        if isSparse:
            return None

        # Round up to next TAR block
        if pastEndOffset % 512 != 0:
            pastEndOffset += 512 - (pastEndOffset % 512)

        return pastEndOffset

    def _tryToMarkAsAppended(self, storedStats: Dict[str, Any], archiveStats: os.stat_result):
        """
        Raises an exception if it makes no sense to only try to go over the new appended data alone
        else sets self.hasBeenAppendedTo to True.
        There is one very specific usecase for which recreating the complete index would be a waste:
        When an uncompressed archive got appended a rather small amount of files.
        """

        # Sizes should be determined and larger or equal
        if (
            not hasattr(archiveStats, "st_size")
            or 'st_size' not in storedStats
            or archiveStats.st_size < storedStats['st_size']
        ):
            raise InvalidIndexError(
                "Will not treat an archive that shrank or has indeterminable size as having been appended to!"
            )

        # Times should be determined and larger or equal
        if (
            not hasattr(archiveStats, "st_mtime")
            or 'st_mtime' not in storedStats
            or archiveStats.st_mtime < storedStats['st_mtime']
        ):
            # Always throw even for if self.verifyModificationTime is False because in this method,
            # the archive should already have been determines as different.
            raise InvalidIndexError(
                f"The modification date for the TAR file {storedStats['st_mtime']} "
                f"is older than the one stored in the SQLite index ({str(archiveStats.st_mtime)})",
            )

        # Checking is expensive and would basically do the same work as creating the database anyway.
        # Therefore, only bother with the added complexity and uncertainty of the randomized index check
        # if the additional part to analyze makes up less than 66% of the total archive.
        #
        # Ignore small archives that don't require much time to process anyway.
        # The threshold is motivated by the benchmarks for "First Mounting".
        # For uncompressed archives, the limiting factor is the number of files.
        # An uncompressed TAR with 1000 64KiB files would take roughly a second.
        if archiveStats.st_size < 64 * 1024 * 1024:
            raise InvalidIndexError("The archive did change but is too small to determine as having been appended to.")

        if self.sqlConnection:
            fileCount = self.sqlConnection.execute('SELECT COUNT(*) FROM "files";').fetchone()[0]
            if archiveStats.st_size < 64 * 1024 * 1024 or fileCount < self.numberOfMetadataToVerify:
                raise InvalidIndexError(
                    "The archive did change but has too few files small to determine as having been appended to."
                )

        # If the archive more than tripled, then the already existing part isn't all that much in
        # comparison to the work that would have to be done anyway. And because the validity check
        # would have to only be an approximation, simply allow the up to 33% overhead to recreate
        # everything from scratch, just to be sure.
        if archiveStats.st_size > 3 * storedStats['st_size']:
            raise InvalidIndexError(
                f"TAR file for this SQLite index has more than tripled in size from "
                f"{storedStats['st_size']} to {archiveStats.st_size}"
            )

        # Note that the xz compressed version of 100k zero-byte files is only ~200KB!
        # But this should be an edge-case and with a compression ratio of ~2, even compressed archives
        # of this size should not take more than 10s, so pretty negligible in my opinion.
        #
        # For compressed archives, detecting appended archives does not help much because the bottleneck is
        # the decompression not the indexing of files. And because indexed_bzip2 and indexed_gzip probably
        # assume that the index is complete once import_index has been called, we have to recreate the full
        # block offsets anyway.
        if self.compression:
            raise InvalidIndexError(
                f"Compressed TAR file for this SQLite index has changed size from "
                f"{storedStats['st_size']} to {archiveStats.st_size}. It cannot be treated as appended."
            )

        if self.sqlConnection:
            indexVersion = self.sqlConnection.execute(
                """SELECT version FROM versions WHERE name == 'index';"""
            ).fetchone()[0]
            if indexVersion != SQLiteIndexedTar.__version__:
                raise InvalidIndexError("Cannot append to index of different versions!")

        if self.printDebug >= 2:
            print("[Info] Archive has probably been appended to because it is larger and more recent.")
        self.hasBeenAppendedTo = True

    def _checkMetadata(self, metadata: Dict[str, Any]) -> None:
        """
        Raises an exception if the metadata mismatches so much that the index has to be treated as incompatible.
        Returns normally and sets self.hasBeenAppendedTo to True if the size of the archive increased but still fits.
        """

        if 'tarstats' in metadata:
            storedStats = json.loads(metadata['tarstats'])
            tarStats = os.stat(self.tarFileName)

            if hasattr(tarStats, "st_size") and 'st_size' in storedStats:
                if tarStats.st_size < storedStats['st_size']:
                    raise InvalidIndexError(
                        f"TAR file for this SQLite index has shrunk in size from "
                        f"{storedStats['st_size']} to {tarStats.st_size}"
                    )

                if tarStats.st_size > storedStats['st_size']:
                    self._tryToMarkAsAppended(storedStats, tarStats)

            # For compressed files, the archive size check should be sufficient because even if the uncompressed
            # size does not change, the compressed size will most likely change.
            # And also it would be expensive to do because the block offsets are not yet loaded yet!
            pastEndOffset = self._getPastEndOffset(self.sqlConnection) if self.sqlConnection else None
            if not self.compression and pastEndOffset:
                # https://pubs.opengroup.org/onlinepubs/9699919799/utilities/pax.html#tag_20_92_13_01
                # > At the end of the archive file there shall be two 512-byte blocks filled with binary zeros,
                # > interpreted as an end-of-archive indicator.
                fileStencil = (self.tarFileObject, pastEndOffset, 1024)
                oldOffset = self.tarFileObject.tell()
                try:
                    with StenciledFile(fileStencils=[fileStencil]) as file:
                        if file.read() != b"\0" * 1024:
                            if self.printDebug >= 2:
                                print(
                                    "[Info] Probably has been appended to because no EOF zero-byte blocks could "
                                    f"be found at offset: {pastEndOffset}"
                                )
                            self._tryToMarkAsAppended(storedStats, tarStats)
                finally:
                    self.tarFileObject.seek(oldOffset)

            # Only happens very rarely, e.g., for more recent files with the same size.
            if (
                not self.hasBeenAppendedTo
                and self.verifyModificationTime
                and hasattr(tarStats, "st_mtime")
                and 'st_mtime' in storedStats
                and tarStats.st_mtime != storedStats['st_mtime']
            ):
                raise InvalidIndexError(
                    f"The modification date for the TAR file {storedStats['st_mtime']} "
                    f"to this SQLite index has changed ({str(tarStats.st_mtime)})",
                )

        # Check arguments used to create the found index.
        # These are only warnings and not forcing a rebuild by default.
        # TODO: Add --force options?
        if 'arguments' in metadata:
            indexArgs = json.loads(metadata['arguments'])
            argumentsToCheck = [
                'mountRecursively',
                'gzipSeekPointSpacing',
                'encoding',
                'stripRecursiveTarExtension',
                'transformRecursiveMountPoint',
                'ignoreZeros',
            ]
            differingArgs = []
            for arg in argumentsToCheck:
                if arg in indexArgs and hasattr(self, arg) and indexArgs[arg] != getattr(self, arg):
                    differingArgs.append((arg, indexArgs[arg], getattr(self, arg)))
            if differingArgs:
                print("[Warning] The arguments used for creating the found index differ from the arguments ")
                print("[Warning] given for mounting the archive now. In order to apply these changes, ")
                print("[Warning] recreate the index using the --recreate-index option!")
                for arg, oldState, newState in differingArgs:
                    print(f"[Warning] {arg}: index: {oldState}, current: {newState}")

    def loadIndex(self, indexFilePath: AnyStr) -> None:
        """Loads the given index SQLite database and checks it for validity raising an exception if it is invalid."""
        if self.indexIsLoaded():
            return

        self.sqlConnection = self._openSqlDb(indexFilePath)
        tables = SQLiteIndexedTar._getSqliteTables(self.sqlConnection)
        versions = None
        try:
            rows = self.sqlConnection.execute('SELECT * FROM versions;')
            versions = {}
            for row in rows:
                versions[row[0]] = (row[2], row[3], row[4])
        except sqlite3.OperationalError:
            pass

        try:
            # Check indexes created with bugged bz2 decoder (bug existed when I did not store versions yet)
            if 'bzip2blocks' in tables and 'versions' not in tables:
                raise InvalidIndexError(
                    "The indexes created with version 0.3.0 through 0.3.3 for bzip2 compressed archives "
                    "are very likely to be wrong because of a bzip2 decoder bug.\n"
                    "Please delete the index or call ratarmount with the --recreate-index option!"
                )

            # Check for empty or incomplete indexes. Pretty safe to rebuild the index for these as they
            # are so invalid, noone should miss them. So, recreate index by default for these cases.
            if 'files' not in tables:
                raise InvalidIndexError("SQLite index is empty")

            if 'filestmp' in tables or 'parentfolders' in tables:
                raise InvalidIndexError("SQLite index is incomplete")

            # Check for pre-sparse support indexes
            if (
                'versions' not in tables
                or 'index' not in versions
                or len(versions['index']) < 2
                or versions['index'][1] < 2
            ):
                print("[Warning] The found outdated index does not contain any sparse file information.")
                print("[Warning] The index will also miss data about multiple versions of a file.")
                print("[Warning] Please recreate the index if you have problems with those.")

            if 'metadata' in tables:
                metadata = dict(self.sqlConnection.execute('SELECT * FROM metadata;'))
                self._checkMetadata(metadata)

        except Exception as e:
            # indexIsLoaded checks self.sqlConnection, so close it before returning because it was found to be faulty
            try:
                self.sqlConnection.close()
            except sqlite3.Error:
                pass
            self.sqlConnection = None

            raise e

        if self.printDebug >= 1:
            print(f"Successfully loaded offset dictionary from {str(indexFilePath)}")

    def _tryLoadIndex(self, indexFilePath: AnyStr) -> bool:
        """calls loadIndex if index is not loaded already and provides extensive error handling"""

        if self.indexIsLoaded():
            return True

        if not os.path.isfile(indexFilePath):
            return False

        try:
            self.loadIndex(indexFilePath)
        except Exception as exception:
            if self.printDebug >= 3:
                traceback.print_exc()

            print("[Warning] Could not load file:", indexFilePath)
            print("[Info] Exception:", exception)
            print("[Info] Some likely reasons for not being able to load the index file:")
            print("[Info]   - The index file has incorrect read permissions")
            print("[Info]   - The index file is incomplete because ratarmount was killed during index creation")
            print("[Info]   - The index file was detected to contain errors because of known bugs of older versions")
            print("[Info]   - The index file got corrupted because of:")
            print("[Info]     - The program exited while it was still writing the index because of:")
            print("[Info]       - the user sent SIGINT to force the program to quit")
            print("[Info]       - an internal error occurred while writing the index")
            print("[Info]       - the disk filled up while writing the index")
            print("[Info]     - Rare lowlevel corruptions caused by hardware failure")

            print("[Info] This might force a time-costly index recreation, so if it happens often")
            print("       and mounting is slow, try to find out why loading fails repeatedly,")
            print("       e.g., by opening an issue on the public github page.")

            try:
                os.remove(indexFilePath)
            except OSError:
                print("[Warning] Failed to remove corrupted old cached index file:", indexFilePath)

        if self.printDebug >= 3 and self.indexIsLoaded():
            print("Loaded index", indexFilePath)

        return self.indexIsLoaded()

    def _checkIndexValidity(self) -> bool:
        if not self.sqlConnection:
            raise IndexNotOpenError("This method can not be called without an opened index database!")

        # Check some of the first and last files in the archive and some random selection in between.
        result = self.sqlConnection.execute(
            f"""
            SELECT * FROM ( SELECT * FROM files ORDER BY offset ASC LIMIT 100 )
            UNION
            SELECT * FROM ( SELECT * FROM files ORDER BY RANDOM() LIMIT {self.numberOfMetadataToVerify} )
            UNION
            SELECT * FROM ( SELECT * FROM files ORDER BY offset DESC LIMIT 100 )
            ORDER BY offset
        """
        )

        t0 = time.time()

        oldOffset = self.tarFileObject.tell()
        try:
            for row in result:
                # As for the stencil size, 512 B (one TAR block) would be enough for most cases except for
                # features like GNU LongLink which store additional metadata in further TAR blocks.
                offset_header = int(row[2])
                with StenciledFile(fileStencils=[(self.tarFileObject, offset_header, 2 * 512)]) as file:
                    with tarfile.open(fileobj=file, mode='r|', ignore_zeros=True, encoding=self.encoding) as archive:
                        tarInfo = next(iter(archive))
                        realFileInfos, _, _ = _TarFileMetadataReader._processTarInfo(
                            tarInfo,
                            file,  # only used for isGnuIncremental == True
                            "",  # pathPrefix
                            offset_header,  # will be added to all offsets to get the real offset
                            self.isGnuIncremental,
                            False,  # mountRecursively
                            self.printDebug,
                        )

                        # Bool columns will have been converted to int 0 or 1 when reading from SQLite.
                        # In order to compare with the read result correctly, we need to convert them to bool, too.
                        storedFileInfo = list(row)
                        for index in [-1, -2]:
                            if storedFileInfo[index] not in [0, 1]:
                                return False
                            storedFileInfo[index] = bool(storedFileInfo[index])

                        if tuple(storedFileInfo) != realFileInfos[0]:
                            return False

            return True
        except tarfile.TarError:
            # Not even worth warning because this simply might happen if the index is not valid anymore.
            return False
        finally:
            self.tarFileObject.seek(oldOffset)

            if self.printDebug >= 2:
                t1 = time.time()
                print(f"[Info] Verifying metadata for {self.numberOfMetadataToVerify + 200} files took {t1-t0:.3f} s")

        return False

    @staticmethod
    def _detectCompression(
        fileobj: IO[bytes], prioritizedBackends: Optional[List[str]], printDebug: int = 0
    ) -> Optional[str]:
        if not isinstance(fileobj, io.IOBase) or not fileobj.seekable():
            return None

        oldOffset = fileobj.tell()
        for compressionId, compression in TAR_COMPRESSION_FORMATS.items():
            # The header check is a necessary condition not a sufficient condition.
            # Especially for gzip, which only has 2 magic bytes, false positives might happen.
            # Therefore, only use the magic bytes based check if the module could not be found
            # in order to still be able to print pinpoint error messages.
            matches = compression.checkHeader(fileobj)
            fileobj.seek(oldOffset)
            if not matches:
                continue

            formatOpen = findAvailableOpen(compressionId, prioritizedBackends)
            if formatOpen:
                return compressionId

            try:
                compressedFileobj = formatOpen(fileobj)
                # Reading 1B from a single-frame zst file might require decompressing it fully in order
                # to get uncompressed file size! Avoid that. The magic bytes should suffice mostly.
                # TODO: Make indexed_zstd not require the uncompressed size for the read call.
                if compressionId != 'zst':
                    compressedFileobj.read(1)
                compressedFileobj.close()
                fileobj.seek(oldOffset)
                return compressionId
            except Exception as e:
                if printDebug >= 2:
                    print(f"[Warning] A given file with magic bytes for {compressionId} could not be opened because:")
                    print(e)
                fileobj.seek(oldOffset)

        return None

    @staticmethod
    def _detectTar(fileobj: IO[bytes], encoding: str, printDebug: int = 0) -> bool:
        if not isinstance(fileobj, io.IOBase) or not fileobj.seekable():
            return False

        oldOffset = fileobj.tell()
        isTar = False
        try:
            with tarfile.open(fileobj=fileobj, mode='r:', encoding=encoding):
                isTar = True
        except (tarfile.ReadError, tarfile.CompressionError):
            if printDebug >= 3:
                print("[Info] File object", fileobj, "is not a TAR.")

        fileobj.seek(oldOffset)
        return isTar

    @staticmethod
    def _openCompressedFile(
        fileobj: IO[bytes],
        gzipSeekPointSpacing: int,
        encoding: str,
        parallelization: int,
        prioritizedBackends: Optional[List[str]],
        printDebug: int = 0,
    ) -> Any:
        """
        Opens a file possibly undoing the compression.
        Returns (tar_file_obj, raw_file_obj, compression, isTar).
        raw_file_obj will be none if compression is None.
        """
        compression = SQLiteIndexedTar._detectCompression(
            fileobj, prioritizedBackends=prioritizedBackends, printDebug=printDebug
        )
        if printDebug >= 3:
            print(f"[Info] Detected compression {compression} for file object:", fileobj)

        if compression not in TAR_COMPRESSION_FORMATS:
            return fileobj, None, compression, SQLiteIndexedTar._detectTar(fileobj, encoding, printDebug=printDebug)

        formatOpen = findAvailableOpen(compression, prioritizedBackends)
        if not formatOpen:
            moduleNames = [module.name for module in TAR_COMPRESSION_FORMATS[compression].modules]
            raise CompressionError(
                f"Cannot open a {compression} compressed TAR file '{fileobj.name}' "
                f"without any of these modules: {moduleNames}"
            )

        if compression == 'gz':
            # The buffer size must be much larger than the spacing or else there will be large performance penalties
            # even for reading sequentially, see https://github.com/pauldmccarthy/indexed_gzip/issues/89
            # Use 4x spacing because each raw read seeks from the last index point even if the position did not change
            # since the last read call. On average, this incurs an overhead of spacing / 2. For 3x spacing, this
            # overhead would be 1/6 = 17%, which should be negligible. The increased memory-usage is not an issue
            # because internally many buffers are allocated with 4 * spacing size.
            bufferSize = max(3 * 1024 * 1024, 3 * gzipSeekPointSpacing)
            # drop_handles keeps a file handle opening as is required to call tell() during decoding
            tar_file = indexed_gzip.IndexedGzipFile(
                fileobj=fileobj, drop_handles=False, spacing=gzipSeekPointSpacing, buffer_size=bufferSize
            )
        elif compression == 'bz2':
            tar_file = indexed_bzip2.open(fileobj, parallelization=parallelization)
        elif (
            compression == 'xz'
            and xz
            and parallelization != 1
            and hasattr(fileobj, 'name')
            and os.path.isfile(fileobj.name)
            and platform.system() == 'Linux'
        ):
            tar_file = formatOpen(fileobj)
            if len(tar_file.block_boundaries) > 1:
                tar_file.close()
                tar_file = ParallelXZReader(fileobj.name, parallelization=parallelization)
        else:
            tar_file = formatOpen(fileobj)

        return tar_file, fileobj, compression, SQLiteIndexedTar._detectTar(tar_file, encoding, printDebug=printDebug)

    @staticmethod
    def _uncheckedRemove(path: Optional[AnyStr]):
        """
        Often cleanup is good manners but it would only be obnoxious if ratarmount crashed on unnecessary cleanup.
        """
        if not path or not os.path.exists(path):
            return

        try:
            os.remove(path)
        except Exception:
            print("[Warning] Could not remove:", path)

    def _clearCompressionOffsets(self):
        if not self.sqlConnection:
            raise IndexNotOpenError("This method can not be called without an opened index database!")

        for table in ['bzip2blocks', 'gzipindex', 'gzipindexes', 'zstdblocks']:
            self.sqlConnection.execute(f"DROP TABLE IF EXISTS {table}")

    def _loadOrStoreCompressionOffsets(self):
        """
        Will load block offsets from SQLite database to backend if a fitting table exists.
        Else it will force creation and store the block offsets of the compression backend into a new table.
        """
        if not self.indexFilePath or self.indexFilePath == ':memory:':
            if self.printDebug >= 2:
                print("[Info] Will skip storing compression seek data because the database is in memory.")
                print("[Info] If the database is in memory, then this data will not be read anyway.")
            return

        # This should be called after the TAR file index is complete (loaded or created).
        # If the TAR file index was created, then tarfile has iterated over the whole file once
        # and therefore completed the implicit compression offset creation.
        if not self.sqlConnection:
            raise IndexNotOpenError("This method can not be called without an opened index database!")
        db = self.sqlConnection
        fileObject = self.tarFileObject

        if (
            hasattr(fileObject, 'set_block_offsets')
            and hasattr(fileObject, 'block_offsets')
            and self.compression in ['bz2', 'zst']
        ):
            if self.compression == 'bz2':
                table_name = 'bzip2blocks'
            elif self.compression == 'zst':
                table_name = 'zstdblocks'

            try:
                offsets = dict(db.execute(f"SELECT blockoffset,dataoffset FROM {table_name};"))
                fileObject.set_block_offsets(offsets)
            except Exception as exception:
                if self.printDebug >= 2:
                    print(f"[Info] Could not load {self.compression} block offset data. Will create it from scratch.")
                    print(exception)
                if self.printDebug >= 3:
                    traceback.print_exc()

                tables = SQLiteIndexedTar._getSqliteTables(db)
                if table_name in tables:
                    db.execute(f"DROP TABLE {table_name}")
                db.execute(f"CREATE TABLE {table_name} ( blockoffset INTEGER PRIMARY KEY, dataoffset INTEGER )")
                db.executemany(f"INSERT INTO {table_name} VALUES (?,?)", fileObject.block_offsets().items())
                db.commit()
            return

        if (
            # fmt: off
            hasattr( fileObject, 'import_index' )
            and hasattr( fileObject, 'export_index' )
            and self.compression == 'gz'
            # fmt: on
        ):
            tables = SQLiteIndexedTar._getSqliteTables(db)

            # The maximum blob size configured by SQLite is exactly 1 GB, see https://www.sqlite.org/limits.html
            # Therefore, this should be smaller. Another argument for making it smaller is that this blob size
            # will be held fully in memory temporarily.
            # But, making it too small would result in too many non-backwards compatible indexes being created.
            maxBlobSize = 256 * 1024 * 1024  # 256 MiB

            if 'gzipindex' in tables or 'gzipindexes' in tables:
                try:
                    t0 = time.time()
                    # indexed_gzip 1.5.0 added support for pure Python file objects as arguments for the index!
                    table = 'gzipindexes' if 'gzipindexes' in tables else 'gzipindex'
                    fileObject.import_index(fileobj=SQLiteBlobsFile(db, table, 'data', buffer_size=maxBlobSize))

                    # SQLiteBlobFile is rather slow to get parts of a large blob by using substr.
                    # Here are some timings for 4x256 MiB blobs:
                    #   buffer size / MiB | time / s
                    #                 512 | 1.94 1.94 1.90 1.92 1.95
                    #                 256 | 1.94 1.98 1.92 2.02 1.91
                    #                 128 | 2.44 2.37 2.38 2.44 2.47
                    #                  64 | 3.51 3.44 3.47 3.47 3.42
                    #                  32 | 5.66 5.71 5.62 5.57 5.61
                    #                  16 | 10.22 9.88 9.73 9.75 9.91
                    # Writing out blobs to file / s         : 9.40 8.71 8.49 10.60 9.13
                    # Importing block offsets from file / s : 0.47 0.46 0.47 0.46 0.41
                    #   => With proper buffer sizes, avoiding writing out the block offsets can be 5x faster!
                    # It seems to me like substr on blobs does not actually support true seeking :/
                    # The blob is probably always loaded fully into memory and only then is the substring being
                    # calculated. For C, there actually is an incremental blob reading interface but not for Python:
                    #   https://www.sqlite.org/c3ref/blob_open.html
                    #   https://bugs.python.org/issue24905
                    print(f"Loading gzip block offsets took {time.time() - t0:.2f}s")

                    if self.parallelization != 1:
                        self._reloadWithPragzip()
                    return

                except Exception as exception:
                    if self.printDebug >= 1:
                        print(
                            "[Warning] Encountered exception when trying to load gzip block offsets from database",
                            exception,
                        )
                    if self.printDebug >= 3:
                        traceback.print_exc()

            if self.printDebug >= 2:
                print("[Info] Could not load GZip Block offset data. Will create it from scratch.")

            # Transparently force index to be built if not already done so. build_full_index was buggy for me.
            # Seeking from end not supported, so we have to read the whole data in in a loop
            while fileObject.read(1024 * 1024):
                pass

            # Old implementation using a temporary file before copying parts of it into blobs.
            # Tested on 1 GiB of gzip block offset data (32 GiB file with block seek point spacing 1 MiB)
            #   Time / s: 23.251 22.251 23.697 23.230 22.484
            # Timings when using WriteSQLiteBlobs to write directly into the SQLite database.
            #   Time / s: 13.029 14.884 14.110 14.229 13.807

            db.execute('CREATE TABLE gzipindexes ( data BLOB )')

            try:
                with WriteSQLiteBlobs(db, 'gzipindexes', blob_size=maxBlobSize) as gzindex:
                    fileObject.export_index(fileobj=gzindex)
            except indexed_gzip.ZranError as exception:
                db.execute('DROP TABLE IF EXISTS "gzipindexes"')

                print("[Warning] The GZip index required for seeking could not be written to the database!")
                print("[Info] This might happen when you are out of space in your temporary file and at the")
                print("[Info] the index file location. The gzipindex size takes roughly 32kiB per 4MiB of")
                print("[Info] uncompressed(!) bytes (0.8% of the uncompressed data) by default.")

                raise RatarmountError("Could not wrote out the gzip seek database.") from exception

            blobCount = db.execute('SELECT COUNT(*) FROM gzipindexes;').fetchone()[0]
            if blobCount == 0:
                if self.printDebug >= 2:
                    print("[Warning] Did not write out any gzip seek data. This should only happen if the gzip ")
                    print("[Warning] size is smaller than the gzip seek point spacing.")
            elif blobCount == 1:
                # For downwards compatibility
                db.execute('ALTER TABLE gzipindexes RENAME TO gzipindex;')

            db.commit()

            if self.parallelization != 1:
                self._reloadWithPragzip()
            return

        # Note that for xz seeking, loading and storing block indexes is unnecessary because it has an index included!
        if self.compression in [None, 'xz']:
            return

        assert False, (
            f"Could not load or store block offsets for {self.compression} "
            "probably because adding support was forgotten!"
        )

    def joinThreads(self):
        if hasattr(self.tarFileObject, 'join_threads'):
            self.tarFileObject.join_threads()

    def _reloadWithPragzip(self):
        if (
            'pragzip' not in sys.modules
            or self.rawFileObject is None
            or self.compression != 'gz'
            # TODO Currently, only use pragzip when explicitly specified because it is still in development.
            # Note that the runaway memory isn't so much an issue when the index has been created with indexed_gzip
            # because it splits at roughly equal decompressed chunk sizes!
            or 'pragzip' not in self.prioritizedBackends
        ):
            return

        # Check whether indexed_gzip might have a higher priority than pragzip if both are listed.
        if (
            'indexed_gzip' in self.prioritizedBackends
            and 'pragzip' in self.prioritizedBackends
            and self.prioritizedBackends.index('indexed_gzip') < self.prioritizedBackends.index('pragzip')
        ):
            # Low index have higher priority (because normally the list would be checked from lowest indexes).
            return

        # Only allow mounting of real files. Pragzip does work with Python file objects but we don't want to
        # mount recursive archives all with the parallel gzip decoder because then the cores would be oversubscribed!
        # Similarly, small files would result in being wholly cached into memory, which probably isn't what the user
        # had intended by using ratarmount?
        isRealFile = (
            hasattr(self.rawFileObject, 'name') and self.rawFileObject.name and os.path.isfile(self.rawFileObject.name)
        )
        hasMultipleChunks = os.stat(self.rawFileObject.name).st_size >= 4 * self.gzipSeekPointSpacing
        if not isRealFile or not hasMultipleChunks:
            if self.printDebug >= 2:
                print("[Info] Do not reopen with pragzip backend because:")
                if not isRealFile:
                    print("[Info]  - the file to open is a recursive file, which limits the usability of ")
                    print("[Info]    parallel decompression.")
                if not hasMultipleChunks:
                    print("[Info]  - is too small to qualify for parallel decompression.")
            return

        if self.tarFileObject:
            self.tarFileObject.close()

        tables = SQLiteIndexedTar._getSqliteTables(self.sqlConnection)

        if 'gzipindex' not in tables and 'gzipindexes' not in tables:
            return

        if self.printDebug >= 1:
            print("[Info] Reopening the gzip with the pragzip backend...")
        self.tarFileObject = pragzip.PragzipFile(self.rawFileObject, parallelization=self.parallelization)

        table = 'gzipindexes' if 'gzipindexes' in tables else 'gzipindex'
        maxBlobSize = 256 * 1024 * 1024  # 256 MiB
        self.tarFileObject.import_index(SQLiteBlobsFile(self.sqlConnection, table, 'data', buffer_size=maxBlobSize))

        if self.printDebug >= 1:
            print("[Info] Reopened the gzip with the pragzip backend.")
