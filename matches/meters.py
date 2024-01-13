from configparser import ConfigParser
from datetime import datetime
import os
from google.protobuf.json_format import MessageToDict
import json
import grpc

from proto_files import meters_pb2, meters_pb2_grpc


class MetersClient():
    def __init__(self) -> None:
        config_object = ConfigParser()
        # config_object.read(os.path.join(os.getcwd(), "market_config.init"))
        config_object.read("/market-microservice/market_config.init")
        meters_microservice = config_object["METERSMICROSERVICE"]
        self.host = meters_microservice["host"]
        self.port = meters_microservice["port"]
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.stub = meters_pb2_grpc.MetersServiceStub(self.channel)

    def get_measurements(self, startInterval: datetime, limit, device=None):
        startInterval = startInterval.strftime("%Y-%m-%dT%H:%M:%SZ")
        startInterval_split = startInterval.split('-')
        if len(startInterval_split[0]) == 1:
            startInterval = "000"+startInterval
        query_meters = meters_pb2.QueryMeters(startInterval=startInterval, limit=limit, deviceId=device)
        try:
            message = self.stub.RetrieveMeasurement(query_meters)
        except Exception as e:
            exit()
        return MessageToDict(message)

    def get_oldest_entry(self):
        startInterval = datetime.min
        try:
            measurements = self.get_measurements(startInterval=startInterval, limit=1)
        except Exception as e:
            exit()
        if measurements == {}:
            exit()
        active_export = [d for d in measurements["entries"] if d["Field"] == "Active export"]
        active_export = sorted(active_export, key=lambda x: datetime.strptime(x["Date"], "%Y-%m-%dT%H:%M:%SZ"))
        return datetime.strptime(active_export[0]["Date"], "%Y-%m-%dT%H:%M:%SZ")
        # return datetime.strptime("2023-07-24T07:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
