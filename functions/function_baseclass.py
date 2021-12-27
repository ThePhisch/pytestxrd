import logging
import socket
from struct import unpack

from definitions import general_vals, request_codes


class Pytestxrd_Base_Function:
    """
    Implement a basic class for the
    """

    @staticmethod
    def help_str() -> str:
        return "Help has not been defined for this function."

    def __init__(self, socket: socket.socket) -> None:
        self.socket = socket

    def run(self) -> None:
        pass

    def check_response_ok(self) -> bool:
        """
        Checking the response of a request

        For the simplest of requests, the response consists of only 3 components
        -> StreamID
        -> Response Code
        -> an kXR_int32

        this function requests the response, checks the values,
        logs debug/warnings and returns whether everything is_ok
        """
        logging.debug("Request sent, receiving an answer now...")
        is_ok = True
        data = self.socket.recv(4)
        (sid, reqcode) = unpack("!HH", data)
        logging.debug(f"Streamid={sid}, Response Code={reqcode}")
        if reqcode == request_codes.kXR_error:
            logging.warning(f"Response Code {reqcode} indicates an error")
            self.handle_error_response()
            return False
        data = self.socket.recv(4)
        (num,) = unpack("!l", data)
        if sid != general_vals.StreamID:
            logging.warning(f"StreamID {sid} != StreamID")
            is_ok = False
        if reqcode != request_codes.kXR_ok:
            logging.warning(f"Response Code {reqcode} != kXR_ok")
            is_ok = False
        if num != 0:
            logging.warning(f"Number {num} != 0")
            is_ok = False
        return is_ok

    def handle_error_response(self) -> None:
        """
        Handles the response if kXR_error is returned

        -> stream has been read up to kXR_error
        -> begin reading from dlen
        """
        data = self.socket.recv(8)
        (dlen, errnum) = unpack("!ll", data)
        logging.debug(f"Dlen={dlen}, Errnum={errnum}")
        data = self.socket.recv(dlen - 4)
        errmsg: bytes = unpack(f"!{dlen - 4}s", data)[0]
        print(errmsg.decode("UTF-8"))

    @staticmethod
    def err_number_of_arguments(num: int, wanted: int) -> None:
        print(f"Check number of arguments: {num}/{wanted} args given")

    @staticmethod
    def err_number_of_options(num: int, maxi: int) -> None:
        print(f"Check number of options: {num}/maximum of {maxi} options")

    @staticmethod
    def check_options_subset(
        list_opts_given: list[str], opts_allowed: set[str]
    ) -> bool:
        opts_given = set(list_opts_given)
        extraneous_opts = opts_given.difference(opts_allowed)
        if extraneous_opts:
            print(f"The following options were not recognised: {list(extraneous_opts)}")
            return False
        logging.debug(f"All options (given {list_opts_given}) were recognised")
        return True
