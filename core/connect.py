from contextlib import contextmanager
import socket
from struct import pack, unpack
from typing import ContextManager
from definitions import request_codes, general_vals
import os
from functools import reduce

@contextmanager
def connect_xrootd(
    host: str, port: int
) -> ContextManager[socket.socket]:
    s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))  # Connect

    # Initial Handshake
    s.send(pack("!LLLLL", 0, 0, 0, 4, 2012))

    # Login
    # Typed out for better understanding
    to_send: tuple[bytes] = (
        pack("!H", general_vals.reqID),
        pack("!H", request_codes.kXR_login),
        pack(
            "!L", os.getpid()
        ),  # Spec says this should be signed, but perl is unsigned
        pack("8s", os.getenv("USER").encode("UTF-(")),
        pack("!H", request_codes.Ability),
        pack("B", request_codes.kXR_asyncap | 4),  # Unsigned Char
        pack("B", 0),
        pack("!L", 0),
    )

    s.send(reduce(lambda x, y: x + y, to_send))
    try:
        yield s
    finally:
        s.shutdown(socket.SHUT_WR)
        s.close()
