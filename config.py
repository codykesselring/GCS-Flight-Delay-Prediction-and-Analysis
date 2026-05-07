PROJECT_ID  = "project-493921"
BUCKET_NAME = "kesselring_bucket"

BTS_URL = (
    "https://transtats.bts.gov/PREZIP/"
    "On_Time_Reporting_Carrier_On_Time_Performance_"
    "1987_present_{year}_{month}.zip"
)

START_YEAR = 2000
END_YEAR   = 2025

KEEP_COLS = [
    "FlightDate", "Reporting_Airline", "Origin", "Dest",
    "CRSDepTime", "DepTime", "DepDelayMinutes",
    "CRSArrTime", "ArrTime", "ArrDelayMinutes",
    "Cancelled", "CancellationCode", "CarrierDelay",
    "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay",
]

AIRPORT_STATIONS = {
    "ATL": "72219013874",
    "ORD": "72530094846",
    "LAX": "72295023174",
    "DFW": "72259023023",
    "DEN": "72565003017",
}
