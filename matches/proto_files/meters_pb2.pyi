import transactions_pb2 as _transactions_pb2
import market_pb2 as _market_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

from transactions_pb2 import PaymentsResponse
from transactions_pb2 import JsonReceipt
from transactions_pb2 import ListReceipts
from transactions_pb2 import IssuerId
from transactions_pb2 import TransactionResponse
DESCRIPTOR: _descriptor.FileDescriptor

class MeasurementResponse(_message.Message):
    __slots__ = ["Date", "DeviceId", "Field", "Value"]
    DATE_FIELD_NUMBER: _ClassVar[int]
    DEVICEID_FIELD_NUMBER: _ClassVar[int]
    Date: str
    DeviceId: str
    FIELD_FIELD_NUMBER: _ClassVar[int]
    Field: str
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Value: str
    def __init__(self, DeviceId: _Optional[str] = ..., Field: _Optional[str] = ..., Value: _Optional[str] = ..., Date: _Optional[str] = ...) -> None: ...

class MeterEntry(_message.Message):
    __slots__ = ["activeExport", "activeImport", "deviceId", "reactiveCapacitive", "reactiveInductive", "timestamp"]
    ACTIVEEXPORT_FIELD_NUMBER: _ClassVar[int]
    ACTIVEIMPORT_FIELD_NUMBER: _ClassVar[int]
    DEVICEID_FIELD_NUMBER: _ClassVar[int]
    REACTIVECAPACITIVE_FIELD_NUMBER: _ClassVar[int]
    REACTIVEINDUCTIVE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    activeExport: int
    activeImport: int
    deviceId: str
    reactiveCapacitive: int
    reactiveInductive: int
    timestamp: str
    def __init__(self, deviceId: _Optional[str] = ..., activeImport: _Optional[int] = ..., activeExport: _Optional[int] = ..., reactiveInductive: _Optional[int] = ..., reactiveCapacitive: _Optional[int] = ..., timestamp: _Optional[str] = ...) -> None: ...

class MeterResponse(_message.Message):
    __slots__ = ["message", "payments", "status"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PAYMENTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    message: str
    payments: _transactions_pb2.PaymentsResponse
    status: int
    def __init__(self, status: _Optional[int] = ..., payments: _Optional[_Union[_transactions_pb2.PaymentsResponse, _Mapping]] = ..., message: _Optional[str] = ...) -> None: ...

class QueryMeters(_message.Message):
    __slots__ = ["deviceId", "limit", "skip", "startInterval"]
    DEVICEID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    SKIP_FIELD_NUMBER: _ClassVar[int]
    STARTINTERVAL_FIELD_NUMBER: _ClassVar[int]
    deviceId: str
    limit: int
    skip: int
    startInterval: str
    def __init__(self, startInterval: _Optional[str] = ..., deviceId: _Optional[str] = ..., skip: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ["entries", "error", "status"]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[MeasurementResponse]
    error: str
    status: int
    def __init__(self, entries: _Optional[_Iterable[_Union[MeasurementResponse, _Mapping]]] = ..., status: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...
