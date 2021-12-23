import logging
import socket
from definitions import general_vals, request_codes
from functions.function_baseclass import Pytestxrd_Base_Function
from core.connect import send

class Mv(Pytestxrd_Base_Function):
    """
    Implements the mv function
    """

    @staticmethod
    def help_str() -> str:
        return "mv <old_path> <new_path>"

    def __init__(self, args: list[str], socket: socket.socket) -> None:
        super().__init__(socket)
        match args:
            case [oldp, newp]:
                self.oldp = oldp
                self.newp = newp + "X" # to counteract truncation
                self.run()
            case _:
                print(f"Check number of arguments: {len(args)}/2 args given")

    def run(self) -> None:
        """
        Send the mv request to the server

        also includes validation using check_response_ok
        """
        plen = len(self.oldp + self.newp)
        args = (
            request_codes.kXR_mv,
            b"\0"*14,
            len(self.oldp),
            plen,
            f"{self.oldp} {self.newp}".encode("UTF-8"),
        )
        send(
            self.socket,
            f"!H14sHl{plen}s",
            args
        )

        if self.check_response_ok():
            logging.info("mv succeeded.")