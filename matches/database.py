from configparser import ConfigParser
import os

import pymongo


class DatabaseClient():
    def __init__(self) -> None:
        config_object = ConfigParser()
        # config_object.read(os.path.join(os.getcwd(), "market_config.init"))
        config_object.read("/market-microservice/market_config.init")
        dbinfo = config_object["DBINFO"]
        self.client = pymongo.MongoClient(dbinfo["str"])
        self.db = self.client[dbinfo["dbname"]]
        self.matches_collection = self.db[dbinfo["matches_collection"]]
        self.prices_collection = self.db[dbinfo["prices_collection"]]

    def get_last_entry_timestamp(self):
        try:
            last_entry = self.matches_collection.find_one({}, sort=[("timestamp", -1)])
        except:
            exit()
        if last_entry == None:
            return None
        else:
            return last_entry["timestamp"]

    def insert(self, matches):
        try:
            matches_result = self.matches_collection.insert_many(matches)
            # print(matches_result.inserted_ids)
        except Exception as e:
            exit()
        return matches_result

    def get_last_price(self, meter_id):
        try:
            price = self.prices_collection.find_one({"meter_id": meter_id}, sort=[("timestamp", -1)])
        except:
            exit()
        return price
