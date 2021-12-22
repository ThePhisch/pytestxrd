import os

class UI:
    """
    Class to deal with all the input and output
    (except CLI args passed earlier).

    Also includes logic on which command to execute
    """

    def __init__(self, hostname: str, port: int) -> None:
        self.hostname = hostname
        self.port = port
        print(f"Login PID: {os.getpid()} Session ID: <not implemented>")
        return

    def prompt(self) -> None:
        """
        Standard prompt
        """
        input(f"{self.hostname}:{self.port}> ")
        return

    def exiting(self) -> None:
        """
        Exiting pytestxrd
        """
        print("\nExiting")
        return