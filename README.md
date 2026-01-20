# Tramwise

A MicroPython e-paper departure board for Swiss public transport. Displays real-time tram, bus, and train departures on a Raspberry Pi Pico W with a Waveshare 3.7" e-paper display.

## Hardware

- Raspberry Pi Pico 2W
- Waveshare 3.7" e-Paper display (480x280)

## Installation

1. Install MicroPython on your Pico W
2. Copy the contents of `pico/` to your device

## Configuration

1. Copy `pico/config/secrets.template.py` to `secrets.py` and add your WiFi credentials
2. Copy `pico/config/stations.template.py` to `stations.py` and configure your stations

Station names must match exactly as shown on [transport.opendata.ch](https://transport.opendata.ch).

## API

Uses the free [Swiss public transport API](https://transport.opendata.ch) (no authentication required).

## Credits

- Waveshare eInk driver: [pico-epaper](https://github.com/phoreglad/pico-epaper) by phoreglad
- Font: [Jersey](https://github.com/scfried/soft-type-jersey) by scfried (SIL)
- Icons: [Phosphor Icons](https://phosphoricons.com/) (MIT)
- Font converter: [micropython-font-to-py](https://github.com/peterhinch/micropython-font-to-py) by Peter Hinch (MIT)
- Bitmap converter: [epaper-img-converter](https://github.com/phoreglad/epaper-img-converter) by phoreglad
- Inspiration: [Tramli](https://tramli.com/)

## License

MIT