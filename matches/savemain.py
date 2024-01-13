from datetime import datetime, timedelta
from itertools import groupby
import math
from operator import itemgetter
import pymongo
import requests
import json

from classes.bid import Bid
from mid_market_rate import mid_market_rate


def round_dt(dt, delta):
    return datetime.min + math.floor((dt - datetime.min) / delta) * delta


start_timestamp = datetime.strptime("2019-01-01 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
# end_timestamp = datetime.datetime()
# print(start_timestamp)

client = pymongo.MongoClient(
    "mongodb://10.255.33.19:27017/?readPreference=primary&ssl=false&directConnection=true"
)

mydb = client["test"]
collection_name = "VIVA"
mycolllection = mydb[collection_name]
mycolllection2 = mydb[collection_name+"_trx"]

last_entry = mycolllection.find_one({}, sort=[("timestamp", -1)])
# print(last_entry)
start_timestamp = datetime.strptime(
    '2023-06-22T16:45:00Z', "%Y-%m-%dT%H:%M:%SZ"
)
# start_timestamp = last_entry["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ")
# print(start_timestamp)
r = requests.get(f"https://api.comsolve.pt/external/devices/meters/measurement?startInterval={'2023-06-22T16:45:00Z'}&limit=2")
print(r.status_code)
if (r.status_code != 200):
    exit()
response = json.loads(r.text)
print(r.text)
delta = timedelta(minutes=15)

active_export = [d for d in response["entries"] if d["Field"] == "Active export"]
active_export = sorted(active_export, key=itemgetter("DeviceId"))
# print(active_export)
active_export_dif = []
for key, value in groupby(active_export, key=itemgetter("DeviceId")):
    value = list(value)
    if len(value) < 2:
        continue
    if round_dt(dt=datetime.strptime(value[0]["Date"], "%Y-%m-%dT%H:%M:%SZ"), delta=delta) == start_timestamp + delta and round_dt(dt=datetime.strptime(value[1]["Date"], "%Y-%m-%dT%H:%M:%SZ"), delta=delta) == start_timestamp:
        print(int(value[0]["Value"]) - int(value[1]["Value"]))
        active_export_dif.append({"DeviceId": key, "Value": int(value[0]["Value"]) - int(value[1]["Value"])})
    # print(key)
    # print(list(value))
print(active_export_dif)


active_import = [d for d in response["entries"] if d["Field"] == "Active import"]
active_import = sorted(active_import, key=itemgetter("DeviceId"))
actice_import_dif = []
for key, value in groupby(active_import, key=itemgetter("DeviceId")):
    value = list(value)
    if len(value) < 2:
        continue
    if round_dt(dt=datetime.strptime(value[0]["Date"], "%Y-%m-%dT%H:%M:%SZ"), delta=delta) == start_timestamp + delta and round_dt(dt=datetime.strptime(value[1]["Date"], "%Y-%m-%dT%H:%M:%SZ"), delta=delta) == start_timestamp:
        actice_import_dif.append({"DeviceId": key, "Value": int(value[0]["Value"]) - int(value[1]["Value"])})
print(actice_import_dif)
# print(active_import)

list_of_bids = list()
list_of_asks = list()
for e in active_export_dif:
    for i in actice_import_dif:
        if e["DeviceId"] == i["DeviceId"]:
            energy = e["Value"] - i["Value"]
            bid = Bid(
                id=e["DeviceId"],
                sell_price=1,
                buy_price=1,
                consumption=i["Value"],
                production=e["Value"],
                energy=energy,
                timestamp=start_timestamp + delta,
            )
            if energy > 0:
                list_of_bids.append(bid)
            else:
                list_of_asks.append(bid)

print(list_of_asks)
print(list_of_bids)
matches, transactions = mid_market_rate(asks=list_of_asks, bids=list_of_bids)
print(matches)
print(transactions)
result = mycolllection.insert_many(matches)
if (len(transactions) > 0):
    result2 = mycolllection2.insert_many(transactions)
