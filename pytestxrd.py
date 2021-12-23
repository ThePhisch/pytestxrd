# Anton Schwarz
# pytestxrd: conversion of testxrd from perl to python

from core.connect import connect_xrootd
from core.args import cli_args
from core.ui import UI
import os

args_passed = cli_args()

with connect_xrootd(*args_passed) as s:
    ui = UI(*args_passed, s)
    while True:
        try:
            ui.prompt()
        except KeyboardInterrupt:
            ui.exiting()
            break