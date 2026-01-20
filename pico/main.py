# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Copyright (c) 2026 Leander Sabel
# Licensed under the MIT License. See LICENSE
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import time
import config.settings, config.messages
from lib.display import TransportDisplay
from lib.networking import Networking, TransportAPIClient


def main():
    td = TransportDisplay(config.settings.active_display)
    td.draw_loading_screen()
    net = Networking()

    def on_retry(attempt, max_retries, delay):
        msg = config.messages.wifi_retry.format(delay=delay, attempt=attempt, max=max_retries)
        td.display_message(msg)

    def on_reconnect():
        td.display_message(config.messages.wifi_reconnecting)

    connected, result = net.connect_with_retries(on_retry)
    if not connected:
        td.display_message(f'{config.messages.no_wifi}{result}')
        td.display_message(config.messages.shutdown)
        return

    api = TransportAPIClient()

    while True:
        if not net.ensure_connected(on_reconnect, on_retry):
            td.display_message(config.messages.shutdown)
            return

        tramwise_board, api_ok = api.get_tramwise_board()
        td.display_board(tramwise_board, net.is_connected(), api_ok)
        time.sleep(30)


if __name__ == "__main__":
    main()