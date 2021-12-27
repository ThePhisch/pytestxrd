import os
import socket

import functions
from functions.chmod import Chmod
from functions.mv import Mv
from functions.ping import Ping
from functions.dir import Dir
from functions.rm import Rm
from functions.rmdir import Rmdir
from functions.open import Open
from functions.close import Close
from functions.read import Read
from core.connect import login
from core.persist import Persist

class UI:
    """
    Class to deal with all the input and output
    (except CLI args passed earlier).

    Also includes logic on which command to execute
    """

    def __init__(self, hostname: str, port: int, session_id: str, socket: socket.socket, persist: Persist) -> None:
        self.hostname = hostname
        self.port = port
        self.socket = socket
        self.session_id = session_id
        self.persist = persist
        print(f"Login PID: {os.getpid()} Session ID: {self.session_id}")
        return

    def prompt(self) -> None:
        """
        Standard prompt
        """
        command = input(f"{self.hostname}:{self.port}> ")
        match command.split():
            case ["mv", *args]:
                obj = Mv(args, self.socket)
            case ["ping", *args]:
                obj = Ping(args, self.socket)
            case ["chmod", *args]:
                obj = Chmod(args, self.socket)
            case ["dir", *args]:
                obj = Dir(args, self.socket)
            case ["rm", *args]:
                obj = Rm(args, self.socket)
            case ["rmdir", *args]:
                obj = Rmdir(args, self.socket)
            case ["open", *args]:
                obj = Open(args, self.socket, self.persist)
            case ["close", *args]:
                obj = Close(args, self.socket, self.persist)
            case ["read", *args]:
                obj = Read(args, self.socket, self.persist)
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

