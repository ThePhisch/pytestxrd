import logging
import socket
from core.persist import Persist
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

    def __init__(self, args: list[str], socket: socket.socket, persist: Persist) -> None:
        super().__init__(socket)
        match args:
            case [path]:
                self.path = path
                self.mode = "644"
                self.persist = persist
                self.run()
            case [path, mode]:
                self.path = path
                self.mode = mode 
                self.persist = persist
                self.run()
            case _:
                self.err_number_of_arguments(len(args), 1)
            # TODO add options

    def run(self) -> None:
        """
        Send the open request to the server

        also includes extended validation using check_response_ok
        """
        if self.persist.ft_entry_exists(self.path):
            # Checking if it is already open
            logging.warning("Aborting open process.") 
            return

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

        # Receive response
        logging.debug("Request sent, receiving an answer now...")
        data = self.socket.recv(4)
        (sid, reqcode) = unpack("!HH", data)

        logging.debug(f"Streamid={sid}, Response Code={reqcode}")

        # Handle response in case of error
        if reqcode == request_codes.kXR_error:
            logging.warning(f"Response Code {reqcode} indicates an error")
            self.handle_error_response()
            return
        # Handle normal response
        (rlen, fhandle_bytes) = unpack("!l4s", self.socket.recv(8))
        fhandle = int.from_bytes(fhandle_bytes, "little")
        logging.debug(f"Rlen={rlen}, Fhandle={fhandle}")

        # Add to filetable
        self.persist.ft_add_entry(self.path, fhandle)

