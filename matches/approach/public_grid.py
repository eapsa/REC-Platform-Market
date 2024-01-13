import datetime
from bson import ObjectId
from classes.bid import Bid


def public_grid(asks: list[Bid], bids: list[Bid]) -> list():
    matches = list()
    bfg = 0.1624
    stg = 0.03
    for ask in asks:
        match_id = ObjectId()
        time = datetime.datetime.utcnow()
        new_match = {
            "timestamp": ask.timestamp,
            "buyer_id": ask.id,
            "seller_id": 100,
            "energy": abs(ask.energy),
            "price": stg,
            "created_at": time,
            "_id": match_id,
        }
        matches.append(new_match)
    for bid in bids:
        match_id = ObjectId()
        time = datetime.datetime.utcnow()
        new_match = {
            "timestamp": bid.timestamp,
            "buyer_id": 100,
            "seller_id": bid.id,
            "energy": abs(bid.energy),
            "price": bfg,
            "created_at": time,
            "_id": match_id,
        }
        matches.append(new_match)
    return matches
