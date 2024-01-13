import datetime
import json


class Bid:
    id: int
    sell_price: float
    buy_price: float
    consumption: float
    production: float
    energy: float
    timestamp: datetime.datetime

    def __init__(self, id: int, sell_price: float, buy_price: float, consumption: float, production: float, energy: float, timestamp: datetime.datetime) -> None:
        self.id = id
        self.sell_price = sell_price
        self.buy_price = buy_price
        self.consumption = consumption
        self.production = production
        self.energy = energy
        self.timestamp = timestamp

    # def to_json(self) -> json:
    #     return json.dumps(self.__dict__, )

    # def __str__(self) -> str:
    #     return f"Id:{self.id}, Sell price:{self.sell_price}"

    def __repr__(self) -> str:
        return f"\n{self.__dict__}"
