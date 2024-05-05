import bz2
import io
import sys
from _typeshed import StrOrBytesPath, StrPath
from builtins import list as _list  # aliases to avoid name clashes with fields named "type" or "list"
from collections.abc import Callable, Iterable, Iterator, Mapping
from gzip import _ReadableFileobj as _GzipReadableFileobj, _WritableFileobj as _GzipWritableFileobj
from types import TracebackType
from typing import IO, ClassVar, Literal, Protocol, overload
from typing_extensions import Self, TypeAlias, deprecated

__all__ = [
    "TarFile",
    "TarInfo",
    "is_tarfile",
    "TarError",
    "ReadError",
    "CompressionError",
    "StreamError",
    "ExtractError",
    "HeaderError",
    "ENCODING",
    "USTAR_FORMAT",
    "GNU_FORMAT",
    "PAX_FORMAT",
    "DEFAULT_FORMAT",
    "open",
]
if sys.version_info >= (3, 12):
    __all__ += [
        "fully_trusted_filter",
        "data_filter",
        "tar_filter",
        "FilterError",
        "AbsoluteLinkError",
        "OutsideDestinationError",
        "SpecialFileError",
        "AbsolutePathError",
        "LinkOutsideDestinationError",
    ]

_FilterFunction: TypeAlias = Callable[[TarInfo, str], TarInfo | None]
_TarfileFilter: TypeAlias = Literal["fully_trusted", "tar", "data"] | _FilterFunction

class _Fileobj(Protocol):
    def read(self, __size: int) -> bytes: ...
    def write(self, __b: bytes) -> object: ...
    def tell(self) -> int: ...
    def seek(self, __pos: int) -> object: ...
    def close(self) -> object: ...
    # Optional fields:
    # name: str | bytes
    # mode: Literal["rb", "r+b", "wb", "xb"]

class _Bz2ReadableFileobj(bz2._ReadableFileobj):
    def close(self) -> object: ...

class _Bz2WritableFileobj(bz2._WritableFileobj):
    def close(self) -> object: ...

# tar constants
NUL: bytes
BLOCKSIZE: int
RECORDSIZE: int
GNU_MAGIC: bytes
POSIX_MAGIC: bytes

LENGTH_NAME: int
LENGTH_LINK: int
LENGTH_PREFIX: int

REGTYPE: bytes
AREGTYPE: bytes
LNKTYPE: bytes
SYMTYPE: bytes
CONTTYPE: bytes
BLKTYPE: bytes
DIRTYPE: bytes
FIFOTYPE: bytes
CHRTYPE: bytes

GNUTYPE_LONGNAME: bytes
GNUTYPE_LONGLINK: bytes
GNUTYPE_SPARSE: bytes

XHDTYPE: bytes
XGLTYPE: bytes
SOLARIS_XHDTYPE: bytes

USTAR_FORMAT: int
GNU_FORMAT: int
PAX_FORMAT: int
DEFAULT_FORMAT: int

# tarfile constants

SUPPORTED_TYPES: tuple[bytes, ...]
REGULAR_TYPES: tuple[bytes, ...]
GNU_TYPES: tuple[bytes, ...]
PAX_FIELDS: tuple[str, ...]
PAX_NUMBER_FIELDS: dict[str, type]
PAX_NAME_FIELDS: set[str]

ENCODING: str

def open(
    name: StrOrBytesPath | None = None,
    mode: str = "r",
    fileobj: IO[bytes] | None = None,  # depends on mode
    bufsize: int = 10240,
    *,
    format: int | None = ...,
    tarinfo: type[TarInfo] | None = ...,
    dereference: bool | None = ...,
    ignore_zeros: bool | None = ...,
    encoding: str | None = ...,
    errors: str = ...,
    pax_headers: Mapping[str, str] | None = ...,
    debug: int | None = ...,
    errorlevel: int | None = ...,
    compresslevel: int | None = ...,
    preset: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | None = ...,
) -> TarFile: ...

class ExFileObject(io.BufferedReader):
    def __init__(self, tarfile: TarFile, tarinfo: TarInfo) -> None: ...

class TarFile:
    OPEN_METH: ClassVar[Mapping[str, str]]
    name: StrOrBytesPath | None
    mode: Literal["r", "a", "w", "x"]
    fileobj: _Fileobj | None
    format: int | None
    tarinfo: type[TarInfo]
    dereference: bool | None
    ignore_zeros: bool | None
    encoding: str | None
    errors: str
    fileobject: type[ExFileObject]
    pax_headers: Mapping[str, str] | None
    debug: int | None
    errorlevel: int | None
    offset: int  # undocumented
    extraction_filter: _FilterFunction | None
    def __init__(
        self,
        name: StrOrBytesPath | None = None,
        mode: Literal["r", "a", "w", "x"] = "r",
        fileobj: _Fileobj | None = None,
        format: int | None = None,
        tarinfo: type[TarInfo] | None = None,
        dereference: bool | None = None,
        ignore_zeros: bool | None = None,
        encoding: str | None = None,
        errors: str = "surrogateescape",
        pax_headers: Mapping[str, str] | None = None,
        debug: int | None = None,
        errorlevel: int | None = None,
        copybufsize: int | None = None,  # undocumented
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...
    def __iter__(self) -> Iterator[TarInfo]: ...
    @classmethod
    def open(
        cls,
        name: StrOrBytesPath | None = None,
        mode: str = "r",
        fileobj: IO[bytes] | None = None,  # depends on mode
        bufsize: int = 10240,
        *,
        format: int | None = ...,
        tarinfo: type[TarInfo] | None = ...,
        dereference: bool | None = ...,
        ignore_zeros: bool | None = ...,
        encoding: str | None = ...,
        errors: str = ...,
        pax_headers: Mapping[str, str] | None = ...,
        debug: int | None = ...,
        errorlevel: int | None = ...,
    ) -> Self: ...
    @classmethod
    def taropen(
        cls,
        name: StrOrBytesPath | None,
        mode: Literal["r", "a", "w", "x"] = "r",
        fileobj: _Fileobj | None = None,
        *,
        compresslevel: int = ...,
        format: int | None = ...,
        tarinfo: type[TarInfo] | None = ...,
        dereference: bool | None = ...,
        ignore_zeros: bool | None = ...,
        encoding: str | None = ...,
        pax_headers: Mapping[str, str] | None = ...,
        debug: int | None = ...,
        errorlevel: int | None = ...,
    ) -> Self: ...
    @overload
    @classmethod
    def gzopen(
        cls,
        name: StrOrBytesPath | None,
        mode: Literal["r"] = "r",
        fileobj: _GzipReadableFileobj | None = None,
        compresslevel: int = 9,
        *,
        format: int | None = ...,
        tarinfo: type[TarInfo] | None = ...,
        dereference: bool | None = ...,
        ignore_zeros: bool | None = ...,
        encoding: str | None = ...,
        pax_headers: Mapping[str, str] | None = ...,
        debug: int | None = ...,
        errorlevel: int | None = ...,
    ) -> Self: ...
    @overload
    @classmethod
    def gzopen(
        cls,
        name: StrOrBytesPath | None,
        mode: Literal["w", "x"],
        fileobj: _GzipWritableFileobj | None = None,
        compresslevel: int = 9,
        *,
        format: int | None = ...,
        tarinfo: type[TarInfo] | None = ...,
        dereference: bool | None = ...,
        ignore_zeros: bool | None = ...,
        encoding: str | None = ...,
        pax_headers: Mapping[str, str] | None = ...,
        debug: int | None = ...,
        errorlevel: int | None = ...,
    ) -> Self: ...
    @overload
    @classmethod
    def bz2open(
        cls,
        name: StrOrBytesPath | None,
        mode: Literal["w", "x"],
        fileobj: _Bz2WritableFileobj | None = None,
        compresslevel: int = 9,
        *,
        format: int | None = ...,
        tarinfo: type[TarInfo] | None = ...,
        dereference: bool | None = ...,
        ignore_zeros: bool | None = ...,
        encoding: str | None = ...,
        pax_headers: Mapping[str, str] | None = ...,
        debug: int | None = ...,
        errorlevel: int | None = ...,
    ) -> Self: ...
    @overload
    @classmethod
    def bz2open(
        cls,
        name: StrOrBytesPath | None,
        mode: Literal["r"] = "r",
        fileobj: _Bz2ReadableFileobj | None = None,
        compresslevel: int = 9,
        *,
        format: int | None = ...,
        tarinfo: type[TarInfo] | None = ...,
        dereference: bool | None = ...,
        ignore_zeros: bool | None = ...,
        encoding: str | None = ...,
        pax_headers: Mapping[str, str] | None = ...,
        debug: int | None = ...,
        errorlevel: int | None = ...,
    ) -> Self: ...
    @classmethod
    def xzopen(
        cls,
        name: StrOrBytesPath | None,
        mode: Literal["r", "w", "x"] = "r",
        fileobj: IO[bytes] | None = None,
        preset: int | None = None,
        *,
        format: int | None = ...,
        tarinfo: type[TarInfo] | None = ...,
        dereference: bool | None = ...,
        ignore_zeros: bool | None = ...,
        encoding: str | None = ...,
        pax_headers: Mapping[str, str] | None = ...,
        debug: int | None = ...,
        errorlevel: int | None = ...,
    ) -> Self: ...
    def getmember(self, name: str) -> TarInfo: ...
    def getmembers(self) -> _list[TarInfo]: ...
    def getnames(self) -> _list[str]: ...
    def list(self, verbose: bool = True, *, members: _list[TarInfo] | None = None) -> None: ...
    def next(self) -> TarInfo | None: ...
    @overload
    @deprecated(
        "Extracting tar archives without specifying `filter` is deprecated until Python 3.14, when 'data' filter will become the default."
    )
    def extractall(
        self,
        path: StrOrBytesPath = ".",
        members: Iterable[TarInfo] | None = None,
        *,
        numeric_owner: bool = False,
        filter: None = ...,
    ) -> None: ...
    @overload
    def extractall(
        self,
        path: StrOrBytesPath = ".",
        members: Iterable[TarInfo] | None = None,
        *,
        numeric_owner: bool = False,
        filter: _TarfileFilter,
    ) -> None: ...
    @overload
    @deprecated(
        "Extracting tar archives without specifying `filter` is deprecated until Python 3.14, when 'data' filter will become the default."
    )
    def extract(
        self,
        member: str | TarInfo,
        path: StrOrBytesPath = "",
        set_attrs: bool = True,
        *,
        numeric_owner: bool = False,
        filter: None = ...,
    ) -> None: ...
    @overload
    def extract(
        self,
        member: str | TarInfo,
        path: StrOrBytesPath = "",
        set_attrs: bool = True,
        *,
        numeric_owner: bool = False,
        filter: _TarfileFilter,
    ) -> None: ...
    def _extract_member(
        self, tarinfo: TarInfo, targetpath: str, set_attrs: bool = True, numeric_owner: bool = False
    ) -> None: ...  # undocumented
    def extractfile(self, member: str | TarInfo) -> IO[bytes] | None: ...
    def makedir(self, tarinfo: TarInfo, targetpath: StrOrBytesPath) -> None: ...  # undocumented
    def makefile(self, tarinfo: TarInfo, targetpath: StrOrBytesPath) -> None: ...  # undocumented
    def makeunknown(self, tarinfo: TarInfo, targetpath: StrOrBytesPath) -> None: ...  # undocumented
    def makefifo(self, tarinfo: TarInfo, targetpath: StrOrBytesPath) -> None: ...  # undocumented
    def makedev(self, tarinfo: TarInfo, targetpath: StrOrBytesPath) -> None: ...  # undocumented
    def makelink(self, tarinfo: TarInfo, targetpath: StrOrBytesPath) -> None: ...  # undocumented
    def chown(self, tarinfo: TarInfo, targetpath: StrOrBytesPath, numeric_owner: bool) -> None: ...  # undocumented
    def chmod(self, tarinfo: TarInfo, targetpath: StrOrBytesPath) -> None: ...  # undocumented
    def utime(self, tarinfo: TarInfo, targetpath: StrOrBytesPath) -> None: ...  # undocumented
    def add(
        self,
        name: StrPath,
        arcname: StrPath | None = None,
        recursive: bool = True,
        *,
        filter: Callable[[TarInfo], TarInfo | None] | None = None,
    ) -> None: ...
    def addfile(self, tarinfo: TarInfo, fileobj: IO[bytes] | None = None) -> None: ...
    def gettarinfo(
        self, name: StrOrBytesPath | None = None, arcname: str | None = None, fileobj: IO[bytes] | None = None
    ) -> TarInfo: ...
    def close(self) -> None: ...

if sys.version_info >= (3, 9):
    def is_tarfile(name: StrOrBytesPath | IO[bytes]) -> bool: ...

else:
    def is_tarfile(name: StrOrBytesPath) -> bool: ...

class TarError(Exception): ...
class ReadError(TarError): ...
class CompressionError(TarError): ...
class StreamError(TarError): ...
class ExtractError(TarError): ...
class HeaderError(TarError): ...

class FilterError(TarError):
    # This attribute is only set directly on the subclasses, but the documentation guarantees
    # that it is always present on FilterError.
    tarinfo: TarInfo

class AbsolutePathError(FilterError):
    def __init__(self, tarinfo: TarInfo) -> None: ...

class OutsideDestinationError(FilterError):
    def __init__(self, tarinfo: TarInfo, path: str) -> None: ...

class SpecialFileError(FilterError):
    def __init__(self, tarinfo: TarInfo) -> None: ...

class AbsoluteLinkError(FilterError):
    def __init__(self, tarinfo: TarInfo) -> None: ...

class LinkOutsideDestinationError(FilterError):
    def __init__(self, tarinfo: TarInfo, path: str) -> None: ...

def fully_trusted_filter(member: TarInfo, dest_path: str) -> TarInfo: ...
def tar_filter(member: TarInfo, dest_path: str) -> TarInfo: ...
def data_filter(member: TarInfo, dest_path: str) -> TarInfo: ...

class TarInfo:
    name: str
    path: str
    size: int
    mtime: int
    chksum: int
    devmajor: int
    devminor: int
    offset: int
    offset_data: int
    sparse: bytes | None
    tarfile: TarFile | None
    mode: int
    type: bytes
    linkname: str
    uid: int
    gid: int
    uname: str
    gname: str
    pax_headers: Mapping[str, str]
    def __init__(self, name: str = "") -> None: ...
    @classmethod
    def frombuf(cls, buf: bytes | bytearray, encoding: str, errors: str) -> Self: ...
    @classmethod
    def fromtarfile(cls, tarfile: TarFile) -> Self: ...
    @property
    def linkpath(self) -> str: ...
    @linkpath.setter
    def linkpath(self, linkname: str) -> None: ...
    def replace(
        self,
        *,
        name: str = ...,
        mtime: int = ...,
        mode: int = ...,
        linkname: str = ...,
        uid: int = ...,
        gid: int = ...,
        uname: str = ...,
        gname: str = ...,
        deep: bool = True,
    ) -> Self: ...
    def get_info(self) -> Mapping[str, str | int | bytes | Mapping[str, str]]: ...
    def tobuf(self, format: int | None = 2, encoding: str | None = "utf-8", errors: str = "surrogateescape") -> bytes: ...
    def create_ustar_header(
        self, info: Mapping[str, str | int | bytes | Mapping[str, str]], encoding: str, errors: str
    ) -> bytes: ...
    def create_gnu_header(
        self, info: Mapping[str, str | int | bytes | Mapping[str, str]], encoding: str, errors: str
    ) -> bytes: ...
    def create_pax_header(self, info: Mapping[str, str | int | bytes | Mapping[str, str]], encoding: str) -> bytes: ...
    @classmethod
    def create_pax_global_header(cls, pax_headers: Mapping[str, str]) -> bytes: ...
    def isfile(self) -> bool: ...
    def isreg(self) -> bool: ...
    def issparse(self) -> bool: ...
    def isdir(self) -> bool: ...
    def issym(self) -> bool: ...
    def islnk(self) -> bool: ...
    def ischr(self) -> bool: ...
    def isblk(self) -> bool: ...
    def isfifo(self) -> bool: ...
    def isdev(self) -> bool: ...
