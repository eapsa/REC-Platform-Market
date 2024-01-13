from datetime import datetime, timedelta
from database import DatabaseClient
from utils import correct_missing_timestamps
from meters import MetersClient


mc = MetersClient()
db = DatabaseClient()
correct_missing_timestamps(actice_import_missing_timestamp_correction=[{"DeviceId": "es-sms-15", "Value": 1}], active_export_missing_timestamp_correction=[{"DeviceId": "es-sms-15", "Value": 1}],
                           timestamp=datetime.utcnow(), delta=timedelta(minutes=15), db_client=db, meters_client=mc)
# print(mc.get_measurements(startInterval=datetime.strptime("2023-07-20T16:45:01Z", "%Y-%m-%dT%H:%M:%SZ"), limit=1))
