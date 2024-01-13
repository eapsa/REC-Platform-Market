import datetime
from bson import ObjectId
from classes.bid import Bid
from classes.state import State


def static(bids: list[Bid], asks: list[Bid]) -> list():
    matches = list()
    bfg = 0.1624
    stg = 0.03
    static_price = 0.12
    for ask in asks:
        for bid in bids:
            if bid.energy == 0:
                continue
            if ask.energy + bid.energy < 0:
                match_id = ObjectId()
                time = datetime.datetime.utcnow()
                new_match = {
                    "timestamp": bid.timestamp,
                    "buyer_id": ask.id,
                    "seller_id": bid.id,
                    "energy": abs(bid.energy),
                    "price": static_price,
                    "created_at": time,
                    "_id": match_id,
                    "metadata": {
                        "match_id": match_id,
                        "transaction_state": State.Created.value,
                        "updated_at": time
                    }
                }
                matches.append(new_match)
                ask.energy += bid.energy
                bid.energy = 0
            else:
                bid.energy += ask.energy
                match_id = ObjectId()
                time = datetime.datetime.utcnow()
                new_match = {
                    "timestamp": bid.timestamp,
                    "buyer_id": ask.id,
                    "seller_id": bid.id,
                    "energy": abs(ask.energy),
                    "price": static_price,
                    "created_at": time,
                    "_id": match_id,
                    "metadata": {
                        "match_id": match_id,
                        "transaction_state": State.Created.value,
                        "updated_at": time
                    }
                }
                matches.append(new_match)
                ask.energy = 0
                break
        if ask.energy != 0:
            match_id = ObjectId()
            time = datetime.datetime.utcnow()
            new_match = {
                "timestamp": ask.timestamp,
                "buyer_id": ask.id,
                "seller_id": 100,
                "energy": abs(ask.energy),
                "price": bfg,
                "created_at": time,
                "_id": match_id,
            }
            ask.energy = 0
            matches.append(new_match)
    for bid in bids:
        if bid.energy != 0:
            match_id = ObjectId()
            time = datetime.datetime.utcnow()
            new_match = {
                "timestamp": bid.timestamp,
                "buyer_id": 100,
                "seller_id": bid.id,
                "energy": abs(bid.energy),
                "price": stg,
                "created_at": time,
                "_id": match_id,
            }
            bid.energy = 0
            matches.append(new_match)
    return matches
