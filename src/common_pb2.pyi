import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SERVICE_ERROR_NONE: _ClassVar[ServiceError]
    SERVICE_ERROR_UNSPECIFIED: _ClassVar[ServiceError]
    SERVICE_ERROR_NO_RESPONSE: _ClassVar[ServiceError]
    SERVICE_ERROR_TIMEOUT: _ClassVar[ServiceError]
    SERVICE_ERROR_ACCESS_DENIED: _ClassVar[ServiceError]

class GetError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GET_ERROR_NONE: _ClassVar[GetError]
    GET_ERROR_UNSPECIFIED: _ClassVar[GetError]
    GET_ERROR_KEY_DOES_NOT_EXIST: _ClassVar[GetError]
    GET_ERROR_TIMEOUT: _ClassVar[GetError]
    GET_ERROR_COULD_NOT_RESOLVE_DRIVER: _ClassVar[GetError]
    GET_ERROR_COULD_NOT_RESOLVE_ADDR: _ClassVar[GetError]
    GET_ERROR_COULD_NOT_RESOLVE_XREF: _ClassVar[GetError]
    GET_ERROR_ACCESS_DENIED: _ClassVar[GetError]

class SetError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SET_ERROR_NONE: _ClassVar[SetError]
    SET_ERROR_UNSPECIFIED: _ClassVar[SetError]
    SET_ERROR_KEY_DOES_NOT_EXIST: _ClassVar[SetError]
    SET_ERROR_TIMEOUT: _ClassVar[SetError]
    SET_ERROR_COULD_NOT_RESOLVE_DRIVER: _ClassVar[SetError]
    SET_ERROR_COULD_NOT_RESOLVE_ADDR: _ClassVar[SetError]
    SET_ERROR_COULD_NOT_RESOLVE_XREF: _ClassVar[SetError]
    SET_ERROR_ACCESS_DENIED: _ClassVar[SetError]
    SET_ERROR_READ_ONLY: _ClassVar[SetError]
    SET_ERROR_INVALID_VALUE_TYPE: _ClassVar[SetError]

class QueryError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUERY_ERROR_NONE: _ClassVar[QueryError]
    QUERY_ERROR_UNSPECIFIED: _ClassVar[QueryError]
    QUERY_ERROR_TIMEOUT: _ClassVar[QueryError]
    QUERY_ERROR_UNKNOWN_PREFIX: _ClassVar[QueryError]
    QUERY_ERROR_ACCESS_DENIED: _ClassVar[QueryError]

class Dtype(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[Dtype]
    NULL: _ClassVar[Dtype]
    DOUBLE: _ClassVar[Dtype]
    FLOAT: _ClassVar[Dtype]
    INT32: _ClassVar[Dtype]
    INT64: _ClassVar[Dtype]
    UINT32: _ClassVar[Dtype]
    UINT64: _ClassVar[Dtype]
    SINT32: _ClassVar[Dtype]
    SINT64: _ClassVar[Dtype]
    FIXED32: _ClassVar[Dtype]
    FIXED64: _ClassVar[Dtype]
    SFIXED32: _ClassVar[Dtype]
    SFIXED64: _ClassVar[Dtype]
    BOOL: _ClassVar[Dtype]
    STRING: _ClassVar[Dtype]
    BYTES: _ClassVar[Dtype]
    POINT: _ClassVar[Dtype]
    POINT_LIST: _ClassVar[Dtype]
    DEVICE: _ClassVar[Dtype]
    DEVICE_LIST: _ClassVar[Dtype]
    DRIVER: _ClassVar[Dtype]
    DRIVER_XREF: _ClassVar[Dtype]
SERVICE_ERROR_NONE: ServiceError
SERVICE_ERROR_UNSPECIFIED: ServiceError
SERVICE_ERROR_NO_RESPONSE: ServiceError
SERVICE_ERROR_TIMEOUT: ServiceError
SERVICE_ERROR_ACCESS_DENIED: ServiceError
GET_ERROR_NONE: GetError
GET_ERROR_UNSPECIFIED: GetError
GET_ERROR_KEY_DOES_NOT_EXIST: GetError
GET_ERROR_TIMEOUT: GetError
GET_ERROR_COULD_NOT_RESOLVE_DRIVER: GetError
GET_ERROR_COULD_NOT_RESOLVE_ADDR: GetError
GET_ERROR_COULD_NOT_RESOLVE_XREF: GetError
GET_ERROR_ACCESS_DENIED: GetError
SET_ERROR_NONE: SetError
SET_ERROR_UNSPECIFIED: SetError
SET_ERROR_KEY_DOES_NOT_EXIST: SetError
SET_ERROR_TIMEOUT: SetError
SET_ERROR_COULD_NOT_RESOLVE_DRIVER: SetError
SET_ERROR_COULD_NOT_RESOLVE_ADDR: SetError
SET_ERROR_COULD_NOT_RESOLVE_XREF: SetError
SET_ERROR_ACCESS_DENIED: SetError
SET_ERROR_READ_ONLY: SetError
SET_ERROR_INVALID_VALUE_TYPE: SetError
QUERY_ERROR_NONE: QueryError
QUERY_ERROR_UNSPECIFIED: QueryError
QUERY_ERROR_TIMEOUT: QueryError
QUERY_ERROR_UNKNOWN_PREFIX: QueryError
QUERY_ERROR_ACCESS_DENIED: QueryError
UNSPECIFIED: Dtype
NULL: Dtype
DOUBLE: Dtype
FLOAT: Dtype
INT32: Dtype
INT64: Dtype
UINT32: Dtype
UINT64: Dtype
SINT32: Dtype
SINT64: Dtype
FIXED32: Dtype
FIXED64: Dtype
SFIXED32: Dtype
SFIXED64: Dtype
BOOL: Dtype
STRING: Dtype
BYTES: Dtype
POINT: Dtype
POINT_LIST: Dtype
DEVICE: Dtype
DEVICE_LIST: Dtype
DRIVER: Dtype
DRIVER_XREF: Dtype

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Header(_message.Message):
    __slots__ = ("Src", "Dst", "TxnId", "SessionToken", "Time")
    SRC_FIELD_NUMBER: _ClassVar[int]
    DST_FIELD_NUMBER: _ClassVar[int]
    TXNID_FIELD_NUMBER: _ClassVar[int]
    SESSIONTOKEN_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    Src: str
    Dst: str
    TxnId: int
    SessionToken: str
    Time: _timestamp_pb2.Timestamp
    def __init__(self, Src: _Optional[str] = ..., Dst: _Optional[str] = ..., TxnId: _Optional[int] = ..., SessionToken: _Optional[str] = ..., Time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetPair(_message.Message):
    __slots__ = ("Key", "Value", "Dtype", "time", "Error", "ErrorMsg")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Key: str
    Value: str
    Dtype: Dtype
    time: _timestamp_pb2.Timestamp
    Error: GetError
    ErrorMsg: str
    def __init__(self, Key: _Optional[str] = ..., Value: _Optional[str] = ..., Dtype: _Optional[_Union[Dtype, str]] = ..., time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., Error: _Optional[_Union[GetError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class SetPair(_message.Message):
    __slots__ = ("Key", "Value", "Dtype", "Ok", "Error", "ErrorMsg")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Key: str
    Value: str
    Dtype: Dtype
    Ok: bool
    Error: SetError
    ErrorMsg: str
    def __init__(self, Key: _Optional[str] = ..., Value: _Optional[str] = ..., Dtype: _Optional[_Union[Dtype, str]] = ..., Ok: bool = ..., Error: _Optional[_Union[SetError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ("Header", "Keys")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Keys: _Optional[_Iterable[str]] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("Header", "Pairs", "Error", "ErrorMsg")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAIRS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Pairs: _containers.RepeatedCompositeFieldContainer[GetPair]
    Error: ServiceError
    ErrorMsg: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Pairs: _Optional[_Iterable[_Union[GetPair, _Mapping]]] = ..., Error: _Optional[_Union[ServiceError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class SetRequest(_message.Message):
    __slots__ = ("Header", "Pairs")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAIRS_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Pairs: _containers.RepeatedCompositeFieldContainer[SetPair]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Pairs: _Optional[_Iterable[_Union[SetPair, _Mapping]]] = ...) -> None: ...

class SetResponse(_message.Message):
    __slots__ = ("Header", "Pairs", "Error", "ErrorMsg")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAIRS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Pairs: _containers.RepeatedCompositeFieldContainer[SetPair]
    Error: ServiceError
    ErrorMsg: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Pairs: _Optional[_Iterable[_Union[SetPair, _Mapping]]] = ..., Error: _Optional[_Union[ServiceError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class BasicQueryRequest(_message.Message):
    __slots__ = ("Header", "Query")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Query: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Query: _Optional[str] = ...) -> None: ...

class BasicQueryResponse(_message.Message):
    __slots__ = ("Header", "Query", "Results", "Error", "ErrorMsg")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Query: str
    Results: _containers.RepeatedCompositeFieldContainer[Triple]
    Error: QueryError
    ErrorMsg: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Query: _Optional[str] = ..., Results: _Optional[_Iterable[_Union[Triple, _Mapping]]] = ..., Error: _Optional[_Union[QueryError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class DeviceQueryRequest(_message.Message):
    __slots__ = ("Header", "Query", "Names", "Types", "Locations", "ChildTypes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    CHILDTYPES_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Query: str
    Names: _containers.RepeatedScalarFieldContainer[str]
    Types: _containers.RepeatedScalarFieldContainer[str]
    Locations: _containers.RepeatedScalarFieldContainer[str]
    ChildTypes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Query: _Optional[str] = ..., Names: _Optional[_Iterable[str]] = ..., Types: _Optional[_Iterable[str]] = ..., Locations: _Optional[_Iterable[str]] = ..., ChildTypes: _Optional[_Iterable[str]] = ...) -> None: ...

class PointQueryRequest(_message.Message):
    __slots__ = ("Header", "Query", "Device", "Names", "Types", "Locations", "ConsiderDeviceLoc", "Resource", "ParentTypes", "Error", "ErrorMsg")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    CONSIDERDEVICELOC_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    PARENTTYPES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Query: str
    Device: str
    Names: _containers.RepeatedScalarFieldContainer[str]
    Types: _containers.RepeatedScalarFieldContainer[str]
    Locations: _containers.RepeatedScalarFieldContainer[str]
    ConsiderDeviceLoc: bool
    Resource: Dtype
    ParentTypes: _containers.RepeatedScalarFieldContainer[str]
    Error: QueryError
    ErrorMsg: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Query: _Optional[str] = ..., Device: _Optional[str] = ..., Names: _Optional[_Iterable[str]] = ..., Types: _Optional[_Iterable[str]] = ..., Locations: _Optional[_Iterable[str]] = ..., ConsiderDeviceLoc: bool = ..., Resource: _Optional[_Union[Dtype, str]] = ..., ParentTypes: _Optional[_Iterable[str]] = ..., Error: _Optional[_Union[QueryError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("Header", "Query", "Values", "Dtype", "Error", "ErrorMsg")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Query: str
    Values: _containers.RepeatedScalarFieldContainer[str]
    Dtype: Dtype
    Error: QueryError
    ErrorMsg: str
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Query: _Optional[str] = ..., Values: _Optional[_Iterable[str]] = ..., Dtype: _Optional[_Union[Dtype, str]] = ..., Error: _Optional[_Union[QueryError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class Triple(_message.Message):
    __slots__ = ("Subject", "Predicate", "Object")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    Subject: str
    Predicate: str
    Object: str
    def __init__(self, Subject: _Optional[str] = ..., Predicate: _Optional[str] = ..., Object: _Optional[str] = ...) -> None: ...

class MakeDeviceRequest(_message.Message):
    __slots__ = ("Name", "Types", "Locations", "Driver", "OtherProperties")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    DRIVER_FIELD_NUMBER: _ClassVar[int]
    OTHERPROPERTIES_FIELD_NUMBER: _ClassVar[int]
    Name: str
    Types: _containers.RepeatedScalarFieldContainer[str]
    Locations: _containers.RepeatedScalarFieldContainer[str]
    Driver: str
    OtherProperties: _containers.RepeatedCompositeFieldContainer[Triple]
    def __init__(self, Name: _Optional[str] = ..., Types: _Optional[_Iterable[str]] = ..., Locations: _Optional[_Iterable[str]] = ..., Driver: _Optional[str] = ..., OtherProperties: _Optional[_Iterable[_Union[Triple, _Mapping]]] = ...) -> None: ...

class MakePointRequest(_message.Message):
    __slots__ = ("Device", "Name", "Types", "Locations", "Xref", "OtherProperties")
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    XREF_FIELD_NUMBER: _ClassVar[int]
    OTHERPROPERTIES_FIELD_NUMBER: _ClassVar[int]
    Device: str
    Name: str
    Types: _containers.RepeatedScalarFieldContainer[str]
    Locations: _containers.RepeatedScalarFieldContainer[str]
    Xref: str
    OtherProperties: _containers.RepeatedCompositeFieldContainer[Triple]
    def __init__(self, Device: _Optional[str] = ..., Name: _Optional[str] = ..., Types: _Optional[_Iterable[str]] = ..., Locations: _Optional[_Iterable[str]] = ..., Xref: _Optional[str] = ..., OtherProperties: _Optional[_Iterable[_Union[Triple, _Mapping]]] = ...) -> None: ...

class MakeDriverRequest(_message.Message):
    __slots__ = ("Name", "Host", "Port", "Image", "Container")
    NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    Name: str
    Host: str
    Port: str
    Image: str
    Container: str
    def __init__(self, Name: _Optional[str] = ..., Host: _Optional[str] = ..., Port: _Optional[str] = ..., Image: _Optional[str] = ..., Container: _Optional[str] = ...) -> None: ...

class MakeResponse(_message.Message):
    __slots__ = ("Url", "ErrorMsg")
    URL_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Url: str
    ErrorMsg: str
    def __init__(self, Url: _Optional[str] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ("Header", "Query", "Triple")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    TRIPLE_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Query: str
    Triple: Triple
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Query: _Optional[str] = ..., Triple: _Optional[_Union[Triple, _Mapping]] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ("Urls",)
    URLS_FIELD_NUMBER: _ClassVar[int]
    Urls: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, Urls: _Optional[_Iterable[str]] = ...) -> None: ...

class HistoryRequest(_message.Message):
    __slots__ = ("Start", "End", "Keys", "Limit")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    Start: str
    End: str
    Keys: _containers.RepeatedScalarFieldContainer[str]
    Limit: int
    def __init__(self, Start: _Optional[str] = ..., End: _Optional[str] = ..., Keys: _Optional[_Iterable[str]] = ..., Limit: _Optional[int] = ...) -> None: ...

class HisRow(_message.Message):
    __slots__ = ("Timestamp", "Value", "Id")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    Timestamp: str
    Value: float
    Id: str
    def __init__(self, Timestamp: _Optional[str] = ..., Value: _Optional[float] = ..., Id: _Optional[str] = ...) -> None: ...

class HistoryResponse(_message.Message):
    __slots__ = ("Header", "Rows", "Error")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Rows: _containers.RepeatedCompositeFieldContainer[HisRow]
    Error: ServiceError
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Rows: _Optional[_Iterable[_Union[HisRow, _Mapping]]] = ..., Error: _Optional[_Union[ServiceError, str]] = ...) -> None: ...

class RefreshRatesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RefreshRatesResponse(_message.Message):
    __slots__ = ("Error", "ErrorMsg")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    Error: ServiceError
    ErrorMsg: str
    def __init__(self, Error: _Optional[_Union[ServiceError, str]] = ..., ErrorMsg: _Optional[str] = ...) -> None: ...

class SetForecastRequest(_message.Message):
    __slots__ = ("header", "forecast")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FORECAST_FIELD_NUMBER: _ClassVar[int]
    header: Header
    forecast: ForecastEntry
    def __init__(self, header: _Optional[_Union[Header, _Mapping]] = ..., forecast: _Optional[_Union[ForecastEntry, _Mapping]] = ...) -> None: ...

class SetForecastResponse(_message.Message):
    __slots__ = ("header", "id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    header: Header
    id: str
    def __init__(self, header: _Optional[_Union[Header, _Mapping]] = ..., id: _Optional[str] = ...) -> None: ...

class GetForecastRequest(_message.Message):
    __slots__ = ("header", "forecast_id", "point_uri", "start", "end")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FORECAST_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_URI_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    header: Header
    forecast_id: str
    point_uri: str
    start: _timestamp_pb2.Timestamp
    end: _timestamp_pb2.Timestamp
    def __init__(self, header: _Optional[_Union[Header, _Mapping]] = ..., forecast_id: _Optional[str] = ..., point_uri: _Optional[str] = ..., start: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetForecastResponse(_message.Message):
    __slots__ = ("header", "forecasts")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FORECASTS_FIELD_NUMBER: _ClassVar[int]
    header: Header
    forecasts: _containers.RepeatedCompositeFieldContainer[ForecastEntry]
    def __init__(self, header: _Optional[_Union[Header, _Mapping]] = ..., forecasts: _Optional[_Iterable[_Union[ForecastEntry, _Mapping]]] = ...) -> None: ...

class ForecastEntry(_message.Message):
    __slots__ = ("forecast_id", "created_at", "point_uri", "forecast_type", "model", "model_version", "metadata", "values")
    FORECAST_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    POINT_URI_FIELD_NUMBER: _ClassVar[int]
    FORECAST_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    forecast_id: str
    created_at: _timestamp_pb2.Timestamp
    point_uri: str
    forecast_type: str
    model: str
    model_version: str
    metadata: _struct_pb2.Struct
    values: _containers.RepeatedCompositeFieldContainer[ForecastValue]
    def __init__(self, forecast_id: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., point_uri: _Optional[str] = ..., forecast_type: _Optional[str] = ..., model: _Optional[str] = ..., model_version: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., values: _Optional[_Iterable[_Union[ForecastValue, _Mapping]]] = ...) -> None: ...

class ForecastValue(_message.Message):
    __slots__ = ("forecast_id", "created_at", "target_time", "scenario", "value")
    FORECAST_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    TARGET_TIME_FIELD_NUMBER: _ClassVar[int]
    SCENARIO_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    forecast_id: str
    created_at: _timestamp_pb2.Timestamp
    target_time: _timestamp_pb2.Timestamp
    scenario: str
    value: float
    def __init__(self, forecast_id: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., target_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., scenario: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...

class RunRequest(_message.Message):
    __slots__ = ("Header", "Image", "Container", "Args", "Kwargs", "EnvVars", "Timeout")
    class KwargsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class EnvVarsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    ENVVARS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Image: str
    Container: str
    Args: _containers.RepeatedScalarFieldContainer[str]
    Kwargs: _containers.ScalarMap[str, str]
    EnvVars: _containers.ScalarMap[str, str]
    Timeout: int
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Image: _Optional[str] = ..., Container: _Optional[str] = ..., Args: _Optional[_Iterable[str]] = ..., Kwargs: _Optional[_Mapping[str, str]] = ..., EnvVars: _Optional[_Mapping[str, str]] = ..., Timeout: _Optional[int] = ...) -> None: ...

class RunResponse(_message.Message):
    __slots__ = ("Header", "ExitCode", "StdOut", "ErrorMsg", "ReturnValues")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EXITCODE_FIELD_NUMBER: _ClassVar[int]
    STDOUT_FIELD_NUMBER: _ClassVar[int]
    ERRORMSG_FIELD_NUMBER: _ClassVar[int]
    RETURNVALUES_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    ExitCode: int
    StdOut: str
    ErrorMsg: str
    ReturnValues: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., ExitCode: _Optional[int] = ..., StdOut: _Optional[str] = ..., ErrorMsg: _Optional[str] = ..., ReturnValues: _Optional[_Iterable[str]] = ...) -> None: ...

class RegisterIntervalRequest(_message.Message):
    __slots__ = ("Header", "Interval", "Requests", "RunNow")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    RUNNOW_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Interval: int
    Requests: _containers.RepeatedCompositeFieldContainer[RunRequest]
    RunNow: bool
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Interval: _Optional[int] = ..., Requests: _Optional[_Iterable[_Union[RunRequest, _Mapping]]] = ..., RunNow: bool = ...) -> None: ...

class RegisterIntervalReponse(_message.Message):
    __slots__ = ("Header", "IntervalId", "ContainerIds")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INTERVALID_FIELD_NUMBER: _ClassVar[int]
    CONTAINERIDS_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    IntervalId: int
    ContainerIds: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., IntervalId: _Optional[int] = ..., ContainerIds: _Optional[_Iterable[str]] = ...) -> None: ...

class CronRequest(_message.Message):
    __slots__ = ("Header", "CronStr", "Requests", "OnStart")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CRONSTR_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    ONSTART_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    CronStr: str
    Requests: _containers.RepeatedCompositeFieldContainer[RunRequest]
    OnStart: bool
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., CronStr: _Optional[str] = ..., Requests: _Optional[_Iterable[_Union[RunRequest, _Mapping]]] = ..., OnStart: bool = ...) -> None: ...

class CronResponse(_message.Message):
    __slots__ = ("Header", "Ok")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Ok: bool
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Ok: bool = ...) -> None: ...

class RegisterHandlerRequest(_message.Message):
    __slots__ = ("Header", "Event", "Requests")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Event: str
    Requests: _containers.RepeatedCompositeFieldContainer[RunRequest]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Event: _Optional[str] = ..., Requests: _Optional[_Iterable[_Union[RunRequest, _Mapping]]] = ...) -> None: ...

class RegisterHandlerResponse(_message.Message):
    __slots__ = ("Header", "Ok")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Ok: bool
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Ok: bool = ...) -> None: ...

class UnregisterHandlerRequest(_message.Message):
    __slots__ = ("Header", "Event", "Requests")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Event: str
    Requests: _containers.RepeatedCompositeFieldContainer[RunRequest]
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Event: _Optional[str] = ..., Requests: _Optional[_Iterable[_Union[RunRequest, _Mapping]]] = ...) -> None: ...

class UnregisterHandlerResponse(_message.Message):
    __slots__ = ("Header", "Ok")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    Header: Header
    Ok: bool
    def __init__(self, Header: _Optional[_Union[Header, _Mapping]] = ..., Ok: bool = ...) -> None: ...
