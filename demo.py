"""
Tramwise - Tram departure display demo
Fetches and filters tram departures from opendata.ch API
Documentation at https://transport.opendata.ch/docs.html#stationboard
"""

import json
import requests
from datetime import datetime

RESOURCE_URL = 'https://transport.opendata.ch/v1/stationboard'

def fetch_stationboard(station_name: str) -> list[dict]:
    response = requests.get(RESOURCE_URL, params={'station': station_name})
    return response.json()['stationboard']

def parse_departure(datetime_iso8601: str | None, fallback_iso8601: str) -> tuple[str, int]:
    dt = datetime.strptime(datetime_iso8601 or fallback_iso8601, "%Y-%m-%dT%H:%M:%S%z")
    minutes_to_departure = int((dt - datetime.now(dt.tzinfo)).total_seconds() // 60)
    return dt.strftime("%H:%M"), minutes_to_departure

def filter_monitored_departures(stationboard: list[dict], station_config: dict) -> list[dict]:
    departures = []

    for connection in stationboard:
        cat, num, to, lines = connection['category'], connection['number'], connection['to'], station_config['lines']

        if not any(cat == line['category'] and num == line['number'] and to == line['to'] for line in lines):
            continue

        time, mtd = parse_departure(connection['stop']['prognosis']['departure'], connection['stop']['departure'])

        if mtd < station_config['distance']:
            continue

        departures.append({"line": cat + num, "to": to, "time": time, "mtd": mtd})

    return departures

def main():
    with open("config.json", "r") as file:
        config = json.load(file)

    all_departures = {}

    for station_config in config['stations']:
        station_name = station_config['name']
        print(f"Fetching departures for {station_name}...")

        stationboard = fetch_stationboard(station_name)
        departures = filter_monitored_departures(stationboard, station_config)
        all_departures[station_name] = departures

    print(json.dumps(all_departures, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
