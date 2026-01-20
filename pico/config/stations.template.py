# Station configuration for Tramwise
# Copy this file to stations.py and configure your local stations
#
# Find your station names at: https://transport.opendata.ch
# Use the exact station name as shown in the API (e.g., 'Zürich, Paradeplatz')
#
# Configuration options per station:
#   name: Exact station name from transport.opendata.ch
#   rows: Number of departures to display for this station
#   leave_now: Minutes until departure to show "leave now" icon (door)
#   hurry: Minutes until departure to show "hurry" icon (running person)
#   unreachable: Minutes threshold - departures sooner than this are not shown
#   monitored_connections: List of specific lines to monitor (optional filter)
#       category: Transport type - 'T' (tram), 'B' (bus), 'S' (S-Bahn), etc.
#       number: Line number as string (e.g., '10', '781')
#       to: Destination name (must match exactly)

stations = [
    {
        'name': 'Zürich, Paradeplatz',
        'rows': 4,
        'leave_now': 6,
        'hurry': 5,
        'unreachable': 4,
        'monitored_connections': [
            {'category': 'T', 'number': '2', 'to': 'Schlieren, Geissweid'},
            {'category': 'T', 'number': '13', 'to': 'Zürich, Bahnhofstrasse/HB'},
        ],
    },
    # Add more stations as needed:
    # {
    #     'name': 'Another Station',
    #     'rows': 2,
    #     'leave_now': 5,
    #     'hurry': 4,
    #     'unreachable': 3,
    #     'monitored_connections': [
    #         {'category': 'B', 'number': '31', 'to': 'Destination'},
    #     ],
    # },
]