# Anton Schwarz
# pytestxrd: conversion of testxrd from perl to python

import socket
import os
from struct import pack
from functools import reduce

from definitions import request_codes

# hardcoded for now
HOST = "taylor.fritz.box"
PORT = 1094

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # INITIAL HANDSHAKE
    initial_handshake = map(lambda x: pack("!i", x), [0, 0, 0, 4, 2012])
    s.send(reduce(lambda x, y: x + y, initial_handshake))
    data = s.recv(1024)

    # LOGIN
    inputs = [
        pack("!H", request_codes.kXR_login),
        pack("!i", os.getpid()),
        pack("!c", b"0"),
        # pack(">c", os.environ["USER"]),
        pack("!c", b"0"),  # Ability 0, standard (leave for now)
        # pack(">c", request_codes.kXR_login | 4),
        pack("!c", b"0"),
        pack("!c", b"0"),
    ]

    s.send(reduce(lambda a, b: a + b, inputs))


print(repr(data))
