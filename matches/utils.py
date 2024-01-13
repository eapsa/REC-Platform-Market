from configparser import ConfigParser
from copy import copy
from datetime import datetime
from itertools import groupby
import math
from operator import itemgetter
import os

from bson import ObjectId

from database import DatabaseClient
from classes.bid import Bid
from meters import MetersClient


def db_init(db_client: DatabaseClient):
    config_object = ConfigParser()
    # config_object.read(os.path.join(os.getcwd(), "market_config.init"))
    config_object.read("/market-microservice/market_config.init")
    dbinfo = config_object["DBINFO"]
    if dbinfo["matches_collection"] not in db_client.db.list_collection_names():
        print("new db")
        db_client.db.create_collection(
            dbinfo["matches_collection"],
            timeseries={
                "timeField": "timestamp",
                "metaField": "metadata",
                "granularity": "minutes"
            }
        )
    else:
        print("db already exists")
    return


def round_dt(dt, delta):
    return datetime.min + math.floor((dt - datetime.min) / delta) * delta


def get_difference(item_list, timestamp, delta):
    difference = []
    missing_timestamp_correction = []
    for key, value in groupby(item_list, key=itemgetter("DeviceId")):

        value = list(value)
        # if len(value) == 1:

        # print(value[0])
        if len(value) < 2 and round_dt(dt=datetime.strptime(value[0]["Date"], "%Y-%m-%dT%H:%M:%SZ"), delta=delta) == timestamp + delta:
            missing_timestamp_correction.append(value[0])
        elif len(value) < 2:
            continue
        elif round_dt(dt=datetime.strptime(value[0]["Date"], "%Y-%m-%dT%H:%M:%SZ"), delta=delta) != timestamp + delta and round_dt(dt=datetime.strptime(value[1]["Date"], "%Y-%m-%dT%H:%M:%SZ"), delta=delta) == timestamp + delta:
            missing_timestamp_correction.append(value[1])
        elif round_dt(dt=datetime.strptime(value[0]["Date"], "%Y-%m-%dT%H:%M:%SZ"), delta=delta) == timestamp + delta and round_dt(dt=datetime.strptime(value[1]["Date"], "%Y-%m-%dT%H:%M:%SZ"), delta=delta) == timestamp:
            difference.append({"DeviceId": key, "Value": int(value[0]["Value"]) - int(value[1]["Value"])})
    return difference, missing_timestamp_correction


def price_split(meter_id, db_client: DatabaseClient):
    config_object = ConfigParser()
    # config_object.read(os.path.join(os.getcwd(), "market_config.init"))
    config_object.read("/market-microservice/market_config.init")
    prices = config_object["PRICES"]
    price = db_client.get_last_price(meter_id)
    if price != None:
        return price["sell_price"], price["buy_price"]
    else:
        return prices["sell"], prices["buy"]


def correct_missing_timestamps(active_export_missing_timestamp_correction, actice_import_missing_timestamp_correction, timestamp, delta, db_client: DatabaseClient, meters_client: MetersClient):
    matches = []
    for i in range(0, len(actice_import_missing_timestamp_correction)):
        start_measurement = meters_client.get_measurements(startInterval=datetime.min, limit=2, device=actice_import_missing_timestamp_correction[i]["DeviceId"])
        if len(start_measurement["entries"]) != 8 or datetime.strptime(start_measurement["entries"][4]["Date"], "%Y-%m-%dT%H:%M:%SZ") > timestamp:
            continue
        start_measurement = []
        time = copy(timestamp)
        while len(start_measurement) == 0 and time > datetime.min:
            time -= delta
            # print(f"        {time}")
            start_measurement = meters_client.get_measurements(startInterval=time, limit=1, device=actice_import_missing_timestamp_correction[i]["DeviceId"])
            if len(start_measurement) > 0 and round_dt(dt=datetime.strptime(start_measurement["entries"][0]["Date"], "%Y-%m-%dT%H:%M:%SZ"), delta=delta) == timestamp+delta:
                start_measurement = []
        if len(start_measurement) == 0:
            continue
        active_export = [d for d in start_measurement["entries"] if d["Field"] == "Active export"]
        active_import = [d for d in start_measurement["entries"] if d["Field"] == "Active import"]
        energy_export = int(active_export_missing_timestamp_correction[i]["Value"]) - int(active_export[i]["Value"])
        energy_import = int(actice_import_missing_timestamp_correction[i]["Value"]) - int(active_import[i]["Value"])
        energy = energy_export - energy_import

        bfg = 0.1624
        stg = 0.03
        match_id = ObjectId()
        time = datetime.utcnow()
        if energy < 0:
            new_match = {
                "timestamp": timestamp+delta,
                "buyer_id": active_export[i]["DeviceId"],
                "seller_id": 100,
                "energy": abs(energy)/1000,
                "price": bfg,
                "created_at": time,
                "_id": match_id,
                "metadata": {
                    "message": "Start timstamp: " + active_export[i]["Date"]
                }
            }
            matches.append(new_match)
        elif energy > 0:
            new_match = {
                "timestamp": timestamp+delta,
                "buyer_id": 100,
                "seller_id": active_export[i]["DeviceId"],
                "energy": abs(energy)/1000,
                "price": stg,
                "created_at": time,
                "_id": match_id,
                "metadata": {
                    "message": "Start timstamp: " + active_export[i]["Date"]
                }
            }
            matches.append(new_match)
    if len(matches) > 0:
        db_client.insert(matches=matches)
    return


def measurements_to_bids(measurements, timestamp, delta, db_client: DatabaseClient, meters_client: MetersClient):
    active_export = [d for d in measurements["entries"] if d["Field"] == "Active export"]
    active_export = sorted(active_export, key=itemgetter("DeviceId"))
    active_export_difference, active_export_missing_timestamp_correction = get_difference(active_export, timestamp, delta)

    active_import = [d for d in measurements["entries"] if d["Field"] == "Active import"]
    active_import = sorted(active_import, key=itemgetter("DeviceId"))
    actice_import_difference, actice_import_missing_timestamp_correction = get_difference(active_import, timestamp, delta)

    if len(actice_import_missing_timestamp_correction) > 0:
        correct_missing_timestamps(active_export_missing_timestamp_correction, actice_import_missing_timestamp_correction, timestamp, delta, db_client, meters_client)

    list_of_bids = list()
    list_of_asks = list()
    for e in active_export_difference:
        for i in actice_import_difference:
            if e["DeviceId"] == i["DeviceId"]:
                energy = e["Value"] - i["Value"]
                sell_price, buy_price = price_split(meter_id=e["DeviceId"], db_client=db_client)
                bid = Bid(
                    id=e["DeviceId"],
                    sell_price=sell_price,
                    buy_price=buy_price,
                    consumption=i["Value"]/1000,
                    production=e["Value"]/1000,
                    energy=energy/1000,
                    timestamp=timestamp + delta,
                )
                if energy > 0:
                    list_of_bids.append(bid)
                else:
                    list_of_asks.append(bid)
    return list_of_bids, list_of_asks
