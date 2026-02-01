# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Copyright (c) 2026 Leander Sabel
# Licensed under the MIT License. See LICENSE
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import time
import ntptime

import config.settings
from lib.display import TransportDisplay
from lib.networking import Networking, TransportAPIClient


def main():
    display = TransportDisplay(config.settings.active_display)
    net = Networking()
    api = TransportAPIClient()

    while True:
        if not net.is_connected():
            net.connect_to_wifi()
            ntptime.settime()

        board = api.get_tramwise_board()
        display.display_board(board, net.is_connected(), api.api_ok)
        time.sleep(config.settings.refresh_rate)

if __name__ == "__main__":
    main()