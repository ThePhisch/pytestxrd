# Anton Schwarz
# pytestxrd: conversion of testxrd from perl to python

from core.connect import connect_xrootd
from core.args import cli_args
from core.ui import UI
import os

hostname, port = cli_args()

with connect_xrootd(hostname, port) as s:
    ui = UI(hostname, port, s)
    while True:
        try:
            ui.prompt()
        except KeyboardInterrupt:
            ui.exiting()
            break