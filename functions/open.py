import logging
import socket
from definitions import general_vals, request_codes
from functions.function_baseclass import Pytestxrd_Base_Function
from core.connect import send
from struct import unpack

class Open(Pytestxrd_Base_Function):
    """
    Implements the open function
    """

    @staticmethod
    def help_str() -> str:
        return "open\t<path> [<mode>]"

    def __init__(self, args: list[str], socket: socket.socket) -> None:
        super().__init__(socket)
        match args:
            case [path]:
                self.path = path
                self.mode = "644"
                self.run()
            case _:
                self.err_number_of_arguments(len(args), 1)
            # TODO add options

    def run(self) -> None:
        """
        Send the open request to the server

        also includes extended validation using check_response_ok
        """
        # TODO check if it is already open
        plen = len(self.path)
        mode = self.get_mode(self.mode, {request_codes.kXR_ow}) # TODO add mode to read from input
        options = 0 # TODO options
        args = (
            request_codes.kXR_open,
            mode,
            options,
            b"\0"*12,
            plen,
            self.path.encode("UTF-8"),
        )
        send(
            self.socket,
            f"!HHH12sl{plen}s",
            args
        )

        logging.debug("Request sent, receiving an answer now...")
        data = self.socket.recv(4)
        (sid, reqcode) = unpack("!HH", data)

        logging.debug(f"Streamid={sid}, Response Code={reqcode}")
        if reqcode == request_codes.kXR_error:
            logging.warning(f"Response Code {reqcode} indicates an error")
            self.handle_error_response()
            return
        (rlen, fhandle_bytes) = unpack("!l4s", self.socket.recv(8))
        fhandle = int.from_bytes(fhandle_bytes, "little")
        logging.debug(f"Rlen={rlen}, Fhandle={fhandle}")
        # TODO add to filetable
        # TODO create a filetable first lol
