import datetime
from bson import ObjectId
from classes.bid import Bid
from classes.state import State


def mid_market_rate(bids: list[Bid], asks: list[Bid]) -> list():
    matches = list()
    bfg = 0.1624
    stg = 0.03
    cp2p = (bfg+stg)/2
    if len(bids) > 0 and len(asks) > 0:
        total_demand = abs(sum(c.energy for c in asks))
        total_supply = abs(sum(c.energy for c in bids))
        if total_demand < total_supply:
            c_im = cp2p
            c_ex = (total_demand*cp2p +
                    (total_supply-total_demand)*stg)/total_supply
            community_quantity = total_demand / total_supply
            for bid in bids:
                if bid.energy != 0:
                    match_id = ObjectId()
                    time = datetime.datetime.utcnow()
                    new_match = {
                        "timestamp": bid.timestamp,
                        "buyer_id": 100,
                        "seller_id": bid.id,
                        "energy": abs(bid.energy)*(1-community_quantity),
                        "price": stg,
                        "created_at": time,
                        "_id": match_id,
                    }
                    bid.energy -= bid.energy*(1-community_quantity)
                    matches.append(new_match)
        elif total_demand > total_supply:
            c_im = (total_supply*cp2p +
                    (total_demand-total_supply)*bfg)/total_demand
            c_ex = cp2p
            community_quantity = total_supply / total_demand
            for ask in asks:
                if ask.energy != 0:
                    match_id = ObjectId()
                    time = datetime.datetime.utcnow()
                    new_match = {
                        "timestamp": ask.timestamp,
                        "buyer_id": ask.id,
                        "seller_id": 100,
                        "energy": abs(ask.energy)*(1-community_quantity),
                        "price": bfg,
                        "created_at": time,
                        "_id": match_id,
                    }
                    ask.energy -= ask.energy*(1-community_quantity)
                    matches.append(new_match)
        else:
            c_im = cp2p
            c_ex = cp2p
            community_quantity = total_supply / total_demand

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
                        "price": cp2p,
                        "created_at": time,
                        "_id": match_id,
                        "metadata": {
                            "match_id": match_id,
                            "transaction_state": State.Created.value,
                            "updated_at": time
                        }
                    }
                    matches.append(new_match)
                    ask.energy = bid.energy + ask.energy
                    bid.energy = 0
                else:
                    match_id = ObjectId()
                    time = datetime.datetime.utcnow()
                    bid.energy = bid.energy + ask.energy
                    new_match = {
                        "timestamp": bid.timestamp,
                        "buyer_id": ask.id,
                        "seller_id": bid.id,
                        "energy": abs(ask.energy),
                        "price": cp2p,
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
