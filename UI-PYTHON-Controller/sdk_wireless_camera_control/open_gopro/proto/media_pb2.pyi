"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
*
Commands to query and manipulate media files
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
from . import response_generic_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class RequestGetLastCapturedMedia(google.protobuf.message.Message):
    """*
    Get the last captured media filename

    Returns a @ref ResponseLastCapturedMedia
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(self) -> None: ...

global___RequestGetLastCapturedMedia = RequestGetLastCapturedMedia

class ResponseLastCapturedMedia(google.protobuf.message.Message):
    """*
    Message sent in response to a @ref RequestGetLastCapturedMedia

    This contains the complete path of the last captured media. Depending on the type of media captured, it will return:

    - Single photo / video: The single media path
    - Any grouped media: The path to the first captured media in the group
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RESULT_FIELD_NUMBER: builtins.int
    MEDIA_FIELD_NUMBER: builtins.int
    result: response_generic_pb2.EnumResultGeneric.ValueType
    "Was the request successful?"

    @property
    def media(self) -> response_generic_pb2.Media:
        """*
        Last captured media if result is RESULT_SUCCESS. Invalid if result is RESULT_RESOURCE_NOT_AVAILBLE.
        """
    def __init__(
        self,
        *,
        result: response_generic_pb2.EnumResultGeneric.ValueType | None = ...,
        media: response_generic_pb2.Media | None = ...
    ) -> None: ...
    def HasField(
        self, field_name: typing_extensions.Literal["media", b"media", "result", b"result"]
    ) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["media", b"media", "result", b"result"]) -> None: ...

global___ResponseLastCapturedMedia = ResponseLastCapturedMedia
