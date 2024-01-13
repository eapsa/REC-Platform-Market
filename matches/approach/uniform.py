import datetime
from bson import ObjectId
from classes.bid import Bid
from classes.state import State
from line_interception import inteception_asks_with_bids


def uniform(bids: list[Bid], asks: list[Bid]) -> list():
    matches = list()
    bfg = 0.1624
    stg = 0.03
    if len(bids) > 0 and len(asks) > 0:
        bids.sort(key=lambda x: x.sell_price)
        asks.sort(key=lambda x: x.buy_price, reverse=True)
        xc, yc = inteception_asks_with_bids(bids=bids, asks=asks)
        price = 0

        if yc != None:
            price = yc
        bids_i = [i for i in bids if i.sell_price <= price]
        asks_i = [i for i in asks if i.buy_price >= price]

        for ask in asks_i:
            for bid in bids_i:
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
                        "price": price,
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
                        "price": price,
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
    if len(bids) > 0:
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
    if len(asks) > 0:
        for ask in asks:
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
    return matches
