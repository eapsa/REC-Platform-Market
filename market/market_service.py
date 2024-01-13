from configparser import ConfigParser
import datetime
import os
from bson import ObjectId

import pymongo
from proto_files import market_pb2
from proto_files import market_pb2_grpc


class MarketService(market_pb2_grpc.MarketServiceServicer):
    def __init__(self) -> None:
        config_object = ConfigParser()
        # config_object.read(os.path.join(os.getcwd(), "market_config.init"))
        config_object.read("/market-microservice/market_config.init")
        # config_object.read("config.init")
        dbinfo = config_object["DBINFO"]
        self.client = pymongo.MongoClient(dbinfo["str"])
        self.db = self.client[dbinfo["dbname"]]
        self.matches_collection = self.db[dbinfo["matches_collection"]]
        self.prices_collection = self.db[dbinfo["prices_collection"]]

    def GetMatches(self, request: market_pb2.MatchesFilter, context):
        matches_list = self.GetMatchesFromDB(request)
        response = market_pb2.ListMatchResponse()
        for match in matches_list:
            json_response = market_pb2.MatchResponse(
                buyerID=str(match["buyer_id"]),
                sellerID=str(match["seller_id"]),
                energy=match["energy"],
                price=match["price"],
                timestamp=match["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                id=str(match["_id"]),
                createdAt=match["created_at"].strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
            if "metadata" in match:
                metadata = match["metadata"]
                if "transaction_id" in metadata:
                    json_response.transactionID = metadata["transaction_id"]
                if "transaction_state" in metadata:
                    json_response.transactionState = metadata["transaction_state"]
                if "updated_at" in metadata:
                    json_response.createdAt = metadata["updated_at"].strftime("%Y-%m-%dT%H:%M:%SZ")
                if "message" in metadata:
                    json_response.message = metadata["message"]
            response.matches.append(json_response)
        return response

    def UpdatePrices(self, request: market_pb2.ListPricesUpdate, context):
        response = market_pb2.Empty()
        for price in request.prices:
            db_response = self.UpdatePriceDB(request=price)
        return response

    def GetPrices(self, request, context):
        prices_list = self.GetPriceDB(request=request)
        response = market_pb2.ListPrices()
        for price in prices_list:
            json_response = market_pb2.PriceResponse(
                timestamp=price["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                meterID=price["metadata"]["meter_id"],
                sellPrice=price["metadata"]["sell_price"],
                buyPrice=price["metadata"]["buy_price"]
            )
            response.prices.append(json_response)
        return response

    def GetMatchesFromDB(self, request: market_pb2.MatchesFilter):
        query_matches = {}
        time = {}
        limit = 0
        skip = 0
        if request.HasField("limit"):
            limit = request.limit
        if request.HasField("skip"):
            skip = request.skip

        if request.HasField("buyerID"):
            query_matches["buyer_id"] = request.buyerID
        if request.HasField("sellerID"):
            query_matches["seller_id"] = request.sellerID
        if request.HasField("matchID"):
            query_matches["_id"] = ObjectId(request.matchID)

        if request.HasField("startTimestamp"):
            time["$gte"] = datetime.datetime.strptime(request.startTimestamp, "%Y-%m-%dT%H:%M:%SZ")
        if request.HasField("endTimestamp"):
            time["$lt"] = datetime.datetime.strptime(request.endTimestamp, "%Y-%m-%dT%H:%M:%SZ")
        if len(time) > 0:
            query_matches["timestamp"] = time
        if len(request.state) > 0:
            states = []
            for state in request.state:
                states.append(state)
            query_matches["metadata.transaction_state"] = {"$in": states}

        matches_list = list(self.matches_collection.find(query_matches).limit(limit=limit).skip(skip=skip))
        return matches_list

    def UpdatePriceDB(self, request: market_pb2.PriceUpdate):
        config_object = ConfigParser()
        config_object.read("config.init")
        dbinfo = config_object["DBINFO"]
        if dbinfo["prices_collection"] not in self.db.list_collection_names():
            self.db.create_collection(
                dbinfo["prices_collection"],
                timeseries={
                    "timeField": "timestamp",
                    "metaField": "metadata",
                    "granularity": "minutes"
                }
            )

        price = self.prices_collection.find_one({"timestamp": datetime.datetime.strptime(request.timestamp, "%Y-%m-%dT%H:%M:%SZ"), "metadata.meter_id": request.meterID})
        if price != None:
            response = self.prices_collection.update_many({"metadata.id": price["_id"]}, {"$set": {"metadata.sell_price": request.sellPrice, "metadata.buy_price": request.buyPrice}})
        else:
            id = ObjectId()
            response = self.prices_collection.insert_one({"timestamp": datetime.datetime.strptime(request.timestamp, "%Y-%m-%dT%H:%M:%SZ"), "metadata": {"meter_id": request.meterID,
                                                         "sell_price": request.sellPrice, "buy_price": request.buyPrice, "id": id}, "_id": id})
        return response

    def GetPriceDB(self, request: market_pb2.PriceFilter):
        query = {}
        limit = 0
        skip = 0
        if request.HasField("limit"):
            limit = request.limit
        if request.HasField("skip"):
            skip = request.skip
        if request.HasField("startTimestamp"):
            query["$gte"] = datetime.datetime.strptime(request.startTimestamp, "%Y-%m-%dT%H:%M:%SZ")
        if request.HasField("endTimestamp"):
            query["$lt"] = datetime.datetime.strptime(request.endTimestamp, "%Y-%m-%dT%H:%M:%SZ")
        if len(query) > 0:
            query = {"metadata.meter_id": request.meterID, "timestamp": query}
        else:
            query = {"metadata.meter_id": request.meterID}
        response = list(self.prices_collection.find(query, sort=[("timestamp", -1)]).limit(limit).skip(skip))
        return response
