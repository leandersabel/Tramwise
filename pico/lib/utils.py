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