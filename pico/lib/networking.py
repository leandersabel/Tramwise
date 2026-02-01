# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Copyright (c) 2026 Leander Sabel
# Licensed under the MIT License. See LICENSE
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import network, time, requests, ntptime

import config.settings, config.stations
from config import secrets
from lib.data import Connection
from lib.utils import urlencode, safe

class Networking:
    """Handles Wi-Fi connectivity."""

    def __init__(self):
        """Initializes and activates the WLAN interface."""
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.ssid = None

    def connect_to_wifi(self):
        """Connects to the first known Wi-Fi network, if available"""
        available = {net[0].decode() for net in self.wlan.scan()}
        print(available)
        known = available & set(secrets.wifi_networks)

        def __try_network(ssid):
            print(f'Trying to connect to {ssid}')
            self.wlan.connect(ssid, secrets.wifi_networks[ssid])
            deadline = time.time() + config.settings.wifi_connect_timeout
            while time.time() < deadline and not self.wlan.isconnected():
                print(f'Retrying until {deadline}')
                time.sleep(config.settings.wifi_poll_interval)
            return self.wlan.isconnected()

        self.ssid = next((ssid for ssid in known if __try_network(ssid)), None)

    def is_connected(self):
        """Returns True if Wi-Fi is currently connected."""
        return self.wlan.isconnected()


class TransportAPIClient:
    """Client for the Swiss public transport API."""

    def __init__(self):
        """Initializes API client with precomputed URL components."""
        self.stationboard_url = config.settings.api_base_url + config.settings.api_stationboard
        self.fields_query = '&'.join(f'fields[]={f}' for f in config.settings.api_fields)
        self.api_ok = None

    def get_tramwise_board(self):
        """Returns stationboards for all configured stations."""
        self.api_ok = True
        return [self.__get_station_board(s) for s in config.stations.stations]

    def __get_station_board(self, station):
        """Fetches and filters connections for a single station."""
        board = self.__fetch_stationboard(station['name'])
        routes = {(c['category'], c['number'], c['to']) for c in station.get('monitored_connections', [])}
        connections = [Connection.from_json(c, station['thresholds']) for c in board if (c['category'], c['number'], c['to']) in routes] if routes else [Connection.from_json(c, station['thresholds']) for c in board]
        reachable = [c for c in connections if not c.unreachable][:station['rows']]
        return [station['name'], reachable]

    def __fetch_stationboard(self, station_name) -> list:
        """Fetches stationboard from API, returns empty list on error."""
        url = (f'{self.stationboard_url}'
               f'?station={urlencode(station_name)}'
               f'&limit={config.settings.api_query_limit}'
               f'&{self.fields_query}')

        try:
            ntptime.settime()
            response = requests.get(url)
            if response.status_code != 200:
                raise ValueError
            return response.json().get('stationboard', [])
        except (OSError, ValueError):
            self.api_ok = False
            return []
