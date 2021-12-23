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
        data = self.socket.recv(8)
        (sid, reqcode, num) = unpack("!HHl", data)
        logging.debug(f"Streamid={sid}, Response Code={reqcode}, num={num}")
        if sid != general_vals.StreamID:
            logging.warning(f"StreamID {sid} != StreamID")
            is_ok = False
        if reqcode is not request_codes.kXR_ok:
            logging.warning(f"Response Code {reqcode} != kXR_ok")
            is_ok = False
        if num is not 0:
            logging.warning(f"Number {num} != 0")
            is_ok = False

        return is_ok
