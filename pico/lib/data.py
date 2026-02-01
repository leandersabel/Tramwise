# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Copyright (c) 2026 Leander Sabel
# Licensed under the MIT License. See LICENSE
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import time
from lib.utils import safe


def parse_iso_datetime(iso8601: str):
    """Parse ISO 8601 datetime string and return (formatted_time, minutes_until_departure)."""
    year, month, day = int(iso8601[0:4]), int(iso8601[5:7]), int(iso8601[8:10])
    hours, minutes, seconds = int(iso8601[11:13]), int(iso8601[14:16]), int(iso8601[17:19])
    zone = int(iso8601[-4:-2]) if len(iso8601) >= 24 else 0
    mtd = int((time.mktime((year, month, day, hours - zone, minutes, seconds, 0, 0)) - time.time()) / 60)
    return iso8601[11:16], mtd


class Connection:
    """A connection represents a possible journey between two locations."""

    def __init__(self, category: str, number: str, to: str, departure: str, departure_prognosis: str, thresholds: dict):
        self.category, self.number, self.to = category, number, to
        self.departure, self.mtd = parse_iso_datetime(departure_prognosis or departure)
        self.unreachable = self.mtd < thresholds.get('unreachable', 0)
        self.hurry = not self.unreachable and self.mtd < thresholds.get('hurry', 0)
        self.leave_now = not self.hurry and self.mtd <= thresholds.get('leave_now', 0)

    @classmethod
    def from_json(cls, json: str, thresholds: dict):
        """Converts raw API connection data to a Connection object."""
        return cls(json['category'], json['number'], json['to'], json['stop']['departure'], json['stop']['prognosis']['departure'], thresholds)