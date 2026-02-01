from assets import jersey15_24_de, jersey20_29_de

active_display = 'pico_ePaper_37_landscape'
active_stations_config = 'demo'
refresh_rate = 30
display_parameters = {
    'pico_ePaper_37_landscape': {
        'display_width': 480,
        'display_height': 280,
        'font_header_file': jersey20_29_de,
        'font_header_size': 29,
        'font_body_file': jersey15_24_de,
        'font_body_size': 24,
        'margin': 5,
        'columns': {
            'line': 10,
            'destination': 60,
            'icon': 350,
            'time': 380,
        },
    },
}

wifi_connect_timeout = 10
wifi_poll_interval = 0.5

api_base_url = 'https://transport.opendata.ch/v1/'
api_stationboard = 'stationboard'
api_query_limit = 15
api_fields = [
    'stationboard/category',
    'stationboard/number',
    'stationboard/to',
    'stationboard/stop/departure',
    'stationboard/stop/prognosis/departure'
]