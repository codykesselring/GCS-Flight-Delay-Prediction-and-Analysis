import pandas as pd
import requests
import io
import time
from config import KEEP_COLS, BTS_URL

NOAA_URL = (
    "https://www.ncei.noaa.gov/data/local-climatological-data/"
    "access/{year}/{station}.csv"
)

def fetch_bts(year, month):
    url = BTS_URL.format(year=year, month=month)
    try:
        print(f"    Downloading BTS {year}-{month:02d}...")
        resp = requests.get(url, timeout=180)
        resp.raise_for_status()

        import zipfile
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            csv_name = [f for f in z.namelist() if f.endswith(".csv")][0]
            with z.open(csv_name) as csv_file:
                df = pd.read_csv(
                    csv_file,
                    usecols=lambda c: c in KEEP_COLS,
                    low_memory=False,
                    encoding="latin-1"
                )

        print(f"    BTS OK: {len(df):,} rows")
        return df
    except Exception as e:
        print(f"    BTS failed: {e}")
        return None

def clean_bts(df):
    df["FlightDate"]      = pd.to_datetime(df["FlightDate"], errors="coerce")
    df["DepDelayMinutes"] = pd.to_numeric(df["DepDelayMinutes"], errors="coerce").fillna(0)
    df["ArrDelayMinutes"] = pd.to_numeric(df["ArrDelayMinutes"], errors="coerce").fillna(0)
    df["Cancelled"]       = df["Cancelled"].fillna(0).astype(int)
    df["IsDelayed"]       = (df["DepDelayMinutes"] > 15).astype(int)
    df = df.dropna(subset=["FlightDate"])
    return df

def fetch_noaa(station_id, year):
    url = NOAA_URL.format(year=year, station=station_id)
    try:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        df = pd.read_csv(
            io.StringIO(resp.text),
            usecols=["DATE", "HourlyPrecipitation", "HourlyVisibility", "HourlyWindSpeed"],
            low_memory=False
        )
        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
        return df.dropna(subset=["DATE"])
    except Exception:
        return None

def build_daily_weather(airport_stations, year):
    frames = []
    for airport, station_id in airport_stations.items():
        w = fetch_noaa(station_id, year)
        if w is None:
            continue
        for col in ["HourlyPrecipitation", "HourlyVisibility", "HourlyWindSpeed"]:
            w[col] = pd.to_numeric(w[col], errors="coerce")
        w["Date"] = w["DATE"].dt.date
        daily = (
            w.groupby("Date")
             .agg(
                 AvgPrecip    =("HourlyPrecipitation", "mean"),
                 AvgVisibility=("HourlyVisibility",    "mean"),
                 AvgWindSpeed =("HourlyWindSpeed",     "mean"),
             )
             .reset_index()
        )
        daily["Origin"] = airport
        frames.append(daily)
        time.sleep(0.2)
    return pd.concat(frames, ignore_index=True) if frames else None

def enrich_with_weather(flights, weather):
    flights["_date"] = flights["FlightDate"].dt.date
    weather = weather.rename(columns={"Date": "_date"})
    return flights.merge(
        weather, on=["_date", "Origin"], how="left"
    ).drop(columns=["_date"])
