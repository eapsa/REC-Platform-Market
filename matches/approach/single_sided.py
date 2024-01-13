import pandas as pd
import datetime
from bson import ObjectId
from classes.bid import Bid
from classes.state import State


def single_sided(bids: list[Bid], asks: list[Bid]) -> list():
    matches = list()
    bfg = 0.1624
    stg = 0.03
    if len(bids) > 0 and len(asks) > 0:
        total_demand = abs(sum(c.energy for c in asks))
        total_supply = abs(sum(c.energy for c in bids))
        bids.sort(key=lambda x: x.sell_price)
        df_b = pd.DataFrame(b.__dict__ for b in bids)
        df_b["cumsum_energy"] = df_b["energy"].cumsum().abs()
        if total_demand < total_supply:
            price = df_b[df_b.cumsum_energy >= total_demand].iloc[0].sell_price
            community_quantity = 1
        else:
            price = df_b["sell_price"].iat[-1]
            community_quantity = total_supply / total_demand
        if community_quantity != 1:
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
                    ask.energy += abs(ask.energy)*(1-community_quantity)
                    matches.append(new_match)
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
