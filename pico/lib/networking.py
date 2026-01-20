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
from lib.utils import urlencode

class Networking:
    """Handles WiFi connectivity and NTP synchronization."""

    def __init__(self):
        """Initializes and activates the WLAN interface."""
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect_to_wifi(self):
        """Connects to a known WiFi network and syncs time. Returns (success, ssid|available_networks)."""
        available = {net[0].decode() for net in self.wlan.scan()}
        known = available & set(secrets.wifi_networks)

        for ssid in known:
            if self.__try_connect(ssid, secrets.wifi_networks[ssid]):
                try:
                    ntptime.settime()
                except OSError:
                    pass  # NTP sync failed, continue with unsync'd time
                return True, ssid
        return False, available

    def connect_with_retries(self, on_retry=None):
        """Attempt WiFi connection with configurable retries. Returns (success, ssid|networks)."""
        max_retries = config.settings.wifi_max_retries
        retry_delay = config.settings.wifi_retry_delay

        for attempt in range(1, max_retries + 1):
            connected, result = self.connect_to_wifi()
            if connected:
                return True, result

            if attempt < max_retries and on_retry:
                on_retry(attempt, max_retries, retry_delay)
                time.sleep(retry_delay)

        return False, result

    def ensure_connected(self, on_reconnect=None, on_retry=None):
        """Check WiFi and reconnect if lost. Returns True if connected."""
        if self.is_connected():
            return True

        if on_reconnect:
            on_reconnect()
        connected, _ = self.connect_with_retries(on_retry)
        return connected

    def is_connected(self):
        """Returns True if WiFi is currently connected."""
        return self.wlan.isconnected()

    def __try_connect(self, ssid, password):
        """Attempts to connect to a single network with timeout."""
        self.wlan.connect(ssid, password)
        deadline = time.time() + config.settings.wifi_connect_timeout
        while not self.wlan.isconnected() and time.time() < deadline:
            time.sleep(config.settings.wifi_poll_interval)
        return self.wlan.isconnected()


class TransportAPIClient:
    """Client for the Swiss public transport API."""

    def __init__(self):
        """Initializes API client with precomputed URL components."""
        self.stationboard_url = config.settings.api_base_url + config.settings.api_stationboard
        self.fields_query = '&'.join(f'fields[]={f}' for f in config.settings.api_fields)
        self.last_request_ok = True

    def get_tramwise_board(self):
        """Returns (board, api_ok) tuple for all configured stations."""
        self.last_request_ok = True
        board = [self.__get_station_board(s) for s in config.stations.stations]
        return board, self.last_request_ok

    def __get_station_board(self, station):
        """Fetches and filters connections for a single station."""
        stationboard = self.__get_stationboard(station['name'])
        monitored = {(c['category'], c['number'], c['to']) for c in station['monitored_connections']}

        connections = []
        for c in stationboard:
            if (c.get('category'), c.get('number'), c.get('to')) in monitored:
                conn = self.__to_connection(c, station)
                if conn:
                    connections.append(conn)

        reachable = [c for c in connections if not c.unreachable][:station['rows']]
        return [station['name'], reachable]

    @staticmethod
    def __to_connection(c, station):
        """Converts raw API connection data to a Connection object. Returns None on malformed data."""
        try:
            return Connection(
                c['category'], c['number'], c['to'],
                c['stop']['departure'],
                c['stop']['prognosis']['departure'],
                station
            )
        except (KeyError, TypeError):
            return None

    def __get_stationboard(self, station_name) -> list:
        """Fetches stationboard from API, returns empty list on error."""
        url = (f'{self.stationboard_url}?station={urlencode(station_name)}'
               f'&limit={config.settings.api_query_limit}&{self.fields_query}')
        try:
            response = requests.get(url)
            if response.status_code != 200:
                self.last_request_ok = False
                return []
            data = response.json()
            return data.get('stationboard', [])
        except (OSError, ValueError, KeyError):
            self.last_request_ok = False
            return []
