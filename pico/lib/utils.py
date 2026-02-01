# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Copyright (c) 2026 Leander Sabel
# Licensed under the MIT License. See LICENSE
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

SAFE_CHARS = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~'


def urlencode(s):
    """URL-encode a string for use in query parameters."""
    return ''.join(chr(c) if c in SAFE_CHARS else f'%{c:02X}' for c in s.encode('utf-8'))


def safe(func, default=None):
    """Execute func and return its result, or default if any exception occurs."""
    try:
        return func()
    except:
        return default


def get_stations(ssid):
    """Resolve station config for the given SSID, falling back to the default."""
    import config.settings, config.stations
    key = config.stations.ssid_configs.get(ssid, config.settings.default_stations_config)
    return config.stations.configurations[key]