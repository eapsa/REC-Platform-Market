import market_pb2 as _market_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

from market_pb2 import Empty
from market_pb2 import MatchesFilter
from market_pb2 import MatchResponse
from market_pb2 import ListMatchResponse
from market_pb2 import UpdateMatch
from market_pb2 import ListUpdateMatch
from market_pb2 import PriceUpdate
from market_pb2 import PriceFilter
from market_pb2 import PriceResponse
from market_pb2 import ListPrices
from market_pb2 import State
DESCRIPTOR: _descriptor.FileDescriptor
NotPaid: _market_pb2.State
Paid: _market_pb2.State
Sent: _market_pb2.State
Wrong: _market_pb2.State

class IssuerId(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class JsonReceipt(_message.Message):
    __slots__ = ["paymentID", "txID"]
    PAYMENTID_FIELD_NUMBER: _ClassVar[int]
    TXID_FIELD_NUMBER: _ClassVar[int]
    paymentID: str
    txID: str
    def __init__(self, paymentID: _Optional[str] = ..., txID: _Optional[str] = ...) -> None: ...

class ListReceipts(_message.Message):
    __slots__ = ["receipts"]
    RECEIPTS_FIELD_NUMBER: _ClassVar[int]
    receipts: _containers.RepeatedCompositeFieldContainer[JsonReceipt]
    def __init__(self, receipts: _Optional[_Iterable[_Union[JsonReceipt, _Mapping]]] = ...) -> None: ...

class PaymentsResponse(_message.Message):
    __slots__ = ["approach", "json", "transactions"]
    APPROACH_FIELD_NUMBER: _ClassVar[int]
    JSON_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    approach: int
    json: _containers.RepeatedCompositeFieldContainer[_market_pb2.MatchResponse]
    transactions: _containers.RepeatedCompositeFieldContainer[TransactionResponse]
    def __init__(self, approach: _Optional[int] = ..., json: _Optional[_Iterable[_Union[_market_pb2.MatchResponse, _Mapping]]] = ..., transactions: _Optional[_Iterable[_Union[TransactionResponse, _Mapping]]] = ...) -> None: ...

class TransactionResponse(_message.Message):
    __slots__ = ["transaction"]
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    transaction: bytes
    def __init__(self, transaction: _Optional[bytes] = ...) -> None: ...
