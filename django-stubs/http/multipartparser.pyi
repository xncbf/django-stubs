from typing import IO, Any, Dict, Iterator, List, Mapping, Optional, Tuple, Union

from django.http.request import QueryDict
from django.utils.datastructures import ImmutableList, MultiValueDict
from typing_extensions import Literal

class MultiPartParserError(Exception): ...
class InputStreamExhausted(Exception): ...

RAW: Literal["raw"]
FILE: Literal["file"]
FIELD: Literal["field"]

class MultiPartParser:
    def __init__(
        self,
        META: Mapping[str, Any],
        input_data: IO[bytes],
        upload_handlers: Union[List[Any], ImmutableList[Any]],
        encoding: Optional[str] = ...,
    ) -> None: ...
    def parse(self) -> Tuple[QueryDict, MultiValueDict]: ...
    def handle_file_complete(self, old_field_name: str, counters: List[int]) -> None: ...
    def sanitize_file_name(self, file_name: str) -> Optional[str]: ...

class LazyStream:
    length: Optional[int] = ...
    position: int = ...
    def __init__(self, producer: Union[BoundaryIter, ChunkIter], length: Optional[int] = ...) -> None: ...
    def tell(self): ...
    def read(self, size: Optional[int] = ...) -> bytes: ...
    def __next__(self) -> bytes: ...
    def close(self) -> None: ...
    def __iter__(self) -> LazyStream: ...
    def unget(self, bytes: bytes) -> None: ...

class ChunkIter:
    flo: IO[bytes] = ...
    chunk_size: int = ...
    def __init__(self, flo: IO[bytes], chunk_size: int = ...) -> None: ...
    def __next__(self) -> bytes: ...
    def __iter__(self) -> ChunkIter: ...

class InterBoundaryIter:
    def __init__(self, stream: LazyStream, boundary: bytes) -> None: ...
    def __iter__(self) -> InterBoundaryIter: ...
    def __next__(self) -> LazyStream: ...

class BoundaryIter:
    def __init__(self, stream: LazyStream, boundary: bytes) -> None: ...
    def __iter__(self) -> BoundaryIter: ...
    def __next__(self) -> bytes: ...

class Parser:
    def __init__(self, stream: LazyStream, boundary: bytes) -> None: ...
    def __iter__(self) -> Iterator[Tuple[str, Dict[str, Tuple[str, Dict[str, Union[bytes, str]]]], LazyStream]]: ...

def parse_header(line: bytes) -> Tuple[str, Dict[str, Any]]: ...
