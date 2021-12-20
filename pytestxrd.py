# Anton Schwarz
# pytestxrd: conversion of testxrd from perl to python

import socket
from struct import pack
from functools import reduce

# hardcoded for now
HOST = "taylor.fritz.box"
PORT = 1094

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    initial_handshake = map(lambda x: pack(">I", x), [0, 0, 0, 4, 2012])
    s.send(reduce(lambda x, y: x + y, initial_handshake))
    data = s.recv(1024)

print(repr(data))
