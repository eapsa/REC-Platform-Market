from configparser import ConfigParser
import datetime
import os
from bson import ObjectId

import pymongo
from state import State
from proto_files import market_pb2
from proto_files import market_pb2_grpc


class AuthenticatedMarketService(market_pb2_grpc.AuthenticatedMarketService):
    def __init__(self) -> None:
        config_object = ConfigParser()
        # config_object.read(os.path.join(os.getcwd(), "market_config.init"))
        config_object.read("/market-microservice/market_config.init")
        dbinfo = config_object["DBINFO"]
        self.client = pymongo.MongoClient(dbinfo["str"])
        self.db = self.client[dbinfo["dbname"]]
        self.matches_collection = self.db[dbinfo["matches_collection"]]
        self.prices_collection = self.db[dbinfo["prices_collection"]]

    def RetrieveMatches(self, request: market_pb2.MatchesFilter, context):
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
            response.matches.append(json_response)
        return response

    def UpdateMatch(self, request: market_pb2.ListUpdateMatch, context):
        response = market_pb2.Empty()
        self.UpdateMatchDB(request=request)
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
            time["$gte"] = datetime.datetime.strptime(request.start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
        if request.HasField("endTimestamp"):
            time["$lt"] = datetime.datetime.strptime(request.end_timestamp, "%Y-%m-%dT%H:%M:%SZ")
        if len(time) > 0:
            query_matches["timestamp"] = time
        if len(request.state) > 0:
            states = []
            for state in request.state:
                states.append(state)
            query_matches["metadata.transaction_state"] = {"$in": states}
        matches_list = list(self.matches_collection.find(query_matches).limit(limit=limit).skip(skip=skip))
        if request.state == [State.Created.value, State.NotPaid.value] and request.HasField("buyerID") and len(request.ListFields()) == 2:
            ids = [ObjectId(doc['_id']) for doc in matches_list]
            self.matches_collection.update_many({"metadata.match_id": {"$in": ids}}, {"$set": {"metadata.transaction_state": State.Sent.value, "metadata.updated_at": datetime.datetime.utcnow()}})
        return matches_list

    def UpdateMatchDB(self, request: market_pb2.ListUpdateMatch):
        for match in request.matches:
            update = {
                "metadata.transaction_state": match.state,
                "metadata.updated_at": datetime.datetime.utcnow()
            }
            if match.HasField("transactionID"):
                update["metadata.transaction_id"] = match.transactionID
            if match.HasField("message"):
                update["metadata.message"] = match.message
            resp = self.matches_collection.update_many({"metadata.match_id": ObjectId(match.matchID)}, {"$set": update})
        return
