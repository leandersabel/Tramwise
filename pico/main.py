# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Copyright (c) 2026 Leander Sabel
# Licensed under the MIT License. See LICENSE
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import time


import config.settings
from lib.display import TransportDisplay
from lib.networking import Networking, TransportAPIClient
from lib.utils import get_stations


def main():
    display = TransportDisplay(config.settings.active_display)
    net = Networking()
    api = TransportAPIClient()

    while True:
        if not net.is_connected():
            net.connect_to_wifi()

        net.sync_time(config.settings.ntp_sync_interval)
        board = api.get_tramwise_board(get_stations(net.ssid))
        display.display_board(board, net.is_connected(), api.api_ok)
        time.sleep(config.settings.refresh_rate)

if __name__ == "__main__":
    main()