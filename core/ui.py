import os
import socket

import functions
from functions.mv import Mv
from functions.testfunc import Testfunc

class UI:
    """
    Class to deal with all the input and output
    (except CLI args passed earlier).

    Also includes logic on which command to execute
    """

    def __init__(self, hostname: str, port: int, debug: bool, socket: type[socket.socket]) -> None:
        self.hostname = hostname
        self.port = port
        self.socket = socket
        print(f"Login PID: {os.getpid()} Session ID: <not implemented>")
        return

    def prompt(self) -> None:
        """
        Standard prompt
        """
        command = input(f"{self.hostname}:{self.port}> ")
        match command.split():
            case ["mv", *args]:
                obj = Mv(args, self.socket)
            case ["testfunc", *args]:
                obj = Testfunc(args, self.socket)
            case ["help"] | ["help", _]:
                self.get_help()
            case _:
                print(f"Unknown command. Enter 'help' for help.")
        return

    def exiting(self) -> None:
        """
        Exiting pytestxrd
        """
        print("\nExiting")
        return

    def get_help(self) -> None:
        """
        Print a helpscreen
        """
        for f in functions.funclist:
            print(f.help_str())
