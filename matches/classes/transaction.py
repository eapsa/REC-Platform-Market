import datetime
import json

from bson import ObjectId

from classes.state import State


class Transaction:
    matchID: ObjectId
    transactionState: int
    transactionID: str
    updatedAt: datetime.datetime
    buyer_id: int
    seller_id: int

    def __init__(self, matchID: ObjectId, transactionState: State, transactionID: str, updatedAt: datetime.datetime, buyer_id: int, seller_id: int) -> None:
        self.matchID = matchID
        self.transactionID = transactionID
        self.transactionState = transactionState.value
        self.updatedAt = updatedAt
        self.buyer_id = buyer_id
        self.seller_id = seller_id

    def __repr__(self) -> str:
        return f"\n{self.__dict__}"
