import logging
import socket
from definitions import general_vals, request_codes
from functions.function_baseclass import Pytestxrd_Base_Function
from core.connect import send

class Open(Pytestxrd_Base_Function):
    """
    Implements the open function
    """

    @staticmethod
    def help_str() -> str:
        return "open\t<old_path> <new_path>"

    def __init__(self, args: list[str], socket: socket.socket) -> None:
        super().__init__(socket)
        match args:
            case [path]:
                self.path = path
                self.run()
            case _:
                self.err_number_of_arguments(len(args), 1)

    def run(self) -> None:
        """
        Send the open request to the server

        also includes extended validation using check_response_ok
        """
        plen = len(self.path)
        args = (
            request_codes.kXR_open,
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
            logging.info("open succeeded.")

            # TODO work, this isnt done

