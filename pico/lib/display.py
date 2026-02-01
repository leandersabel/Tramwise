# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Copyright (c) 2026 Leander Sabel
# Licensed under the MIT License. See LICENSE
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from framebuf import FrameBuffer, MONO_HLSB

from lib.ePaper import EinkPIO
from lib.writer import Writer

from config import settings
from assets import run_24, door_24, wifi_high_32, wifi_slash_32, globe_32, globe_x_32, tramwise_logo


class Canvas(FrameBuffer):
    """A white-filled framebuffer canvas for drawing."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._buf = bytearray(width * height // 8)
        super().__init__(self._buf, width, height, MONO_HLSB)
        self.fill(1)


def _truncate(text, writer, max_width):
    """Truncate text to fit within max_width pixels, adding '..' if needed."""
    if writer.stringlen(text) <= max_width:
        return text
    while text and writer.stringlen(text + '..') > max_width:
        text = text[:-1]
    return text + '..'


class TransportDisplay:
    """E-paper display controller for rendering transit departure boards."""

    def __init__(self, display_type):
        self.display = EinkPIO(rotation=90)
        self.canvas = Canvas(self.display.width, self.display.height)
        self.params = settings.display_parameters[display_type]

        self.ink_header = Writer(self.canvas, self.params['font_header_file'])
        self.ink_body = Writer(self.canvas, self.params['font_body_file'])

        self.icon_hurry = FrameBuffer(run_24.img_bw, run_24.width, run_24.height, MONO_HLSB)
        self.icon_leave_now = FrameBuffer(door_24.img_bw, door_24.width, door_24.height, MONO_HLSB)
        self.icon_wifi = FrameBuffer(wifi_high_32.img_bw, wifi_high_32.width, wifi_high_32.height, MONO_HLSB)
        self.icon_wifi_off = FrameBuffer(wifi_slash_32.img_bw, wifi_slash_32.width, wifi_slash_32.height, MONO_HLSB)
        self.icon_api = FrameBuffer(globe_32.img_bw, globe_32.width, globe_32.height, MONO_HLSB)
        self.icon_api_off = FrameBuffer(globe_x_32.img_bw, globe_x_32.width, globe_x_32.height, MONO_HLSB)

        self._show_loading_screen()

    def _show_loading_screen(self):
        logo = FrameBuffer(tramwise_logo.img_bw, tramwise_logo.width, tramwise_logo.height, MONO_HLSB)
        self.canvas.blit(logo, 0, 20)
        self.display.blit(self.canvas, 0, 0)
        self.display.show(lut=1)

    def _draw_text(self, x, y, text, writer=None):
        """Draw text at position using the specified writer."""
        writer = writer or self.ink_body
        writer.set_textpos(self.canvas, x, y)
        writer.printstring(text, invert=True)

    def _draw_status_icons(self, wifi_connected, api_connected):
        """Draw status icons in the upper right corner."""
        margin = self.params['margin']
        x = self.params['columns']['time']

        wifi_icon = self.icon_wifi if wifi_connected else self.icon_wifi_off
        self.canvas.blit(wifi_icon, x, 0)

        if api_connected is not None:
            api_icon = self.icon_api if api_connected else self.icon_api_off
            self.canvas.blit(api_icon, x + wifi_high_32.width + margin, 0)

    def _fits_on_canvas(self, x, item_height):
        """Check if an item of given height fits at position x."""
        return x + item_height <= self.canvas.height

    def _render_connection(self, connection, x):
        """Render a single connection row at vertical position x."""
        cols = self.params['columns']

        self._draw_text(x, cols['line'], connection.category + connection.number)
        max_dest = cols['icon'] - cols['destination']
        self._draw_text(x, cols['destination'], _truncate(connection.to, self.ink_body, max_dest))
        self._draw_text(x, cols['time'], f'{connection.departure} ({connection.mtd}\')')

        icon = self.icon_hurry if connection.hurry else (self.icon_leave_now if connection.leave_now else None)
        if icon:
            self.canvas.blit(icon, cols['icon'], x)

    def display_board(self, board: list, wifi_connected=True, api_connected=True):
        """Render the full departure board."""
        self.canvas.fill(1)
        self._draw_status_icons(wifi_connected, api_connected)

        x = self.params['margin']
        header_height = self.params['font_header_size'] + self.params['margin']
        row_height = self.params['font_body_size']

        for name, connections in board:
            if not self._fits_on_canvas(x, header_height):
                break
            max_header = self.params['columns']['icon'] - self.params['margin']
            self._draw_text(x, self.params['margin'], _truncate(name, self.ink_header, max_header), self.ink_header)
            x += header_height

            for connection in connections:
                if not self._fits_on_canvas(x, row_height):
                    break
                self._render_connection(connection, x)
                x += row_height

            x += self.params['margin']

        self.display.blit(self.canvas, 0, 0)
        self.display.show(lut=1)