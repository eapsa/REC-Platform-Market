from datetime import datetime, timedelta
from database import DatabaseClient
from approach.mid_market_rate import mid_market_rate
from utils import db_init, measurements_to_bids, round_dt
from meters import MetersClient


meters_client = MetersClient()
db_client = DatabaseClient()

delta = timedelta(minutes=15)
current_timestamp = round_dt(dt=datetime.utcnow(), delta=delta)

timestamp = db_client.get_last_entry_timestamp()
if timestamp == None:
    db_init(db_client=db_client)
    timestamp = round_dt(dt=meters_client.get_oldest_entry(), delta=delta)

while timestamp != current_timestamp:
    # print(timestamp)
    measurements = meters_client.get_measurements(startInterval=timestamp, limit=2)
    if measurements == {}:
        timestamp += delta
        continue
    bids, asks = measurements_to_bids(measurements=measurements, timestamp=timestamp, delta=delta, db_client=db_client, meters_client=meters_client)
    matches = mid_market_rate(asks=asks, bids=bids)
    timestamp += delta
    if len(matches) > 0:
        result = db_client.insert(matches=matches)
print("end")
