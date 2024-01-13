from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

Created: State
DESCRIPTOR: _descriptor.FileDescriptor
Error: State
NotPaid: State
Paid: State
Sent: State

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListMatchResponse(_message.Message):
    __slots__ = ["matches"]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[MatchResponse]
    def __init__(self, matches: _Optional[_Iterable[_Union[MatchResponse, _Mapping]]] = ...) -> None: ...

class ListPrices(_message.Message):
    __slots__ = ["prices"]
    PRICES_FIELD_NUMBER: _ClassVar[int]
    prices: _containers.RepeatedCompositeFieldContainer[PriceResponse]
    def __init__(self, prices: _Optional[_Iterable[_Union[PriceResponse, _Mapping]]] = ...) -> None: ...

class ListPricesUpdate(_message.Message):
    __slots__ = ["prices"]
    PRICES_FIELD_NUMBER: _ClassVar[int]
    prices: _containers.RepeatedCompositeFieldContainer[PriceUpdate]
    def __init__(self, prices: _Optional[_Iterable[_Union[PriceUpdate, _Mapping]]] = ...) -> None: ...

class ListUpdateMatch(_message.Message):
    __slots__ = ["matches"]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[UpdateMatch]
    def __init__(self, matches: _Optional[_Iterable[_Union[UpdateMatch, _Mapping]]] = ...) -> None: ...

class MatchResponse(_message.Message):
    __slots__ = ["buyerID", "createdAt", "energy", "id", "message", "price", "sellerID", "timestamp", "transactionID", "transactionState", "updatedAt"]
    BUYERID_FIELD_NUMBER: _ClassVar[int]
    CREATEDAT_FIELD_NUMBER: _ClassVar[int]
    ENERGY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    SELLERID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONSTATE_FIELD_NUMBER: _ClassVar[int]
    UPDATEDAT_FIELD_NUMBER: _ClassVar[int]
    buyerID: str
    createdAt: str
    energy: float
    id: str
    message: str
    price: float
    sellerID: str
    timestamp: str
    transactionID: str
    transactionState: State
    updatedAt: str
    def __init__(self, timestamp: _Optional[str] = ..., buyerID: _Optional[str] = ..., sellerID: _Optional[str] = ..., energy: _Optional[float] = ..., price: _Optional[float] = ..., id: _Optional[str] = ..., createdAt: _Optional[str] = ..., transactionID: _Optional[str] = ..., transactionState: _Optional[_Union[State, str]] = ..., updatedAt: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class MatchesFilter(_message.Message):
    __slots__ = ["buyerID", "endTimestamp", "limit", "matchID", "sellerID", "skip", "startTimestamp", "state"]
    BUYERID_FIELD_NUMBER: _ClassVar[int]
    ENDTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    MATCHID_FIELD_NUMBER: _ClassVar[int]
    SELLERID_FIELD_NUMBER: _ClassVar[int]
    SKIP_FIELD_NUMBER: _ClassVar[int]
    STARTTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    buyerID: str
    endTimestamp: str
    limit: int
    matchID: str
    sellerID: str
    skip: int
    startTimestamp: str
    state: _containers.RepeatedScalarFieldContainer[State]
    def __init__(self, buyerID: _Optional[str] = ..., sellerID: _Optional[str] = ..., state: _Optional[_Iterable[_Union[State, str]]] = ..., startTimestamp: _Optional[str] = ..., endTimestamp: _Optional[str] = ..., matchID: _Optional[str] = ..., skip: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class PriceFilter(_message.Message):
    __slots__ = ["endTimestamp", "limit", "meterID", "skip", "startTimestamp"]
    ENDTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    METERID_FIELD_NUMBER: _ClassVar[int]
    SKIP_FIELD_NUMBER: _ClassVar[int]
    STARTTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    endTimestamp: str
    limit: int
    meterID: str
    skip: int
    startTimestamp: str
    def __init__(self, meterID: _Optional[str] = ..., startTimestamp: _Optional[str] = ..., endTimestamp: _Optional[str] = ..., skip: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class PriceResponse(_message.Message):
    __slots__ = ["buyPrice", "meterID", "sellPrice", "timestamp"]
    BUYPRICE_FIELD_NUMBER: _ClassVar[int]
    METERID_FIELD_NUMBER: _ClassVar[int]
    SELLPRICE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    buyPrice: float
    meterID: str
    sellPrice: float
    timestamp: str
    def __init__(self, timestamp: _Optional[str] = ..., meterID: _Optional[str] = ..., sellPrice: _Optional[float] = ..., buyPrice: _Optional[float] = ...) -> None: ...

class PriceUpdate(_message.Message):
    __slots__ = ["buyPrice", "meterID", "sellPrice", "timestamp"]
    BUYPRICE_FIELD_NUMBER: _ClassVar[int]
    METERID_FIELD_NUMBER: _ClassVar[int]
    SELLPRICE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    buyPrice: float
    meterID: str
    sellPrice: float
    timestamp: str
    def __init__(self, timestamp: _Optional[str] = ..., meterID: _Optional[str] = ..., buyPrice: _Optional[float] = ..., sellPrice: _Optional[float] = ...) -> None: ...

class UpdateMatch(_message.Message):
    __slots__ = ["matchID", "message", "state", "transactionID"]
    MATCHID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONID_FIELD_NUMBER: _ClassVar[int]
    matchID: str
    message: str
    state: State
    transactionID: str
    def __init__(self, matchID: _Optional[str] = ..., state: _Optional[_Union[State, str]] = ..., transactionID: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
