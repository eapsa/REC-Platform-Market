import datetime
from bson import ObjectId
from classes.bid import Bid
from classes.state import State


def bill_sharing(bids: list[Bid], asks: list[Bid]) -> list():
    matches = list()
    bfg = 0.1624
    stg = 0.03

    total_demand = abs(sum(c.energy for c in asks))
    total_supply = abs(sum(c.energy for c in bids))
    m = min(total_demand, total_supply)
    e_bfg = total_demand - m
    e_stg = total_supply - m
    c_im = 0
    c_ex = 0
    if total_demand != 0:
        c_im = bfg * (e_bfg/total_demand)
    if total_supply != 0:
        c_ex = stg * (e_stg/total_supply)
    if c_ex != 0:
        for bid in bids:
            c_n = abs(bid.energy)*c_ex
            match_id = ObjectId()
            time = datetime.datetime.utcnow()
            energy = (abs(bid.energy)*c_ex)/stg
            new_match = {
                "timestamp": bid.timestamp,
                "buyer_id": 100,
                "seller_id": bid.id,
                "energy": energy,
                "price": stg,
                "created_at": time,
                "_id": match_id,
            }
            bid.energy -= energy
            matches.append(new_match)
    if c_im != 0:
        for ask in asks:
            c_n = abs(ask.energy)*c_im
            match_id = ObjectId()
            time = datetime.datetime.utcnow()
            energy = (abs(ask.energy)*c_im)/bfg
            new_match = {
                "timestamp": ask.timestamp,
                "buyer_id": ask.id,
                "seller_id": 100,
                "energy": (abs(ask.energy)*c_im)/bfg,
                "price": bfg,
                "created_at": time,
                "_id": match_id,
            }
            ask.energy += energy
            matches.append(new_match)
    if len(bids) > 0 and len(asks) > 0:
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
                            "price": 0,
                            "created_at": time,
                            "_id": match_id,
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
                            "price": 0,
                            "created_at": time,
                            "_id": match_id,
                        }
                        matches.append(new_match)
                        ask.energy = 0
                        break
    return matches
