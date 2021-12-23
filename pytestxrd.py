"""
Anton Schwarz
Main file of pytestxrd: testing utility for xrootd (rewritten from perl)

-> connects to xrootd server (also handles quitting)
-> enters infinite loop with UI prompt (which handles further input)
-> (CLI arguments passed are also dealt with)
"""

from core.connect import connect_xrootd, login
from core.args import cli_args
from core.ui import UI

args_passed = cli_args()

with connect_xrootd(*args_passed) as s:
    session_id = login(s)
    ui = UI(*args_passed, session_id, s)
    while True:
        try:
            ui.prompt()
        except KeyboardInterrupt:
            ui.exiting()
            break