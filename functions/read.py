import logging
import socket
from core.persist import Persist
from definitions import general_vals, request_codes
from functions.function_baseclass import Pytestxrd_Base_Function
from core.connect import send
from struct import unpack

class Read(Pytestxrd_Base_Function):
    """
    Implements the read function
    """

    @staticmethod
    def help_str() -> str:
        return "open\t<path> [<mode>]"

    def __init__(self, args: list[str], socket: socket.socket, persist: Persist) -> None:
        super().__init__(socket)
        match args:
            case [path, offset]:
                self.path = path
                self.offset = min(int(offset), general_vals.maxValidOffset)
                self.length = general_vals.pageSize
            case [path, offset, "*"]:
                self.path = path
                self.offset = min(int(offset), general_vals.maxValidOffset)
                self.length = general_vals.maxValidLength
            case [path, offset, length]:
                self.path = path
                self.offset = min(int(offset), general_vals.maxValidOffset)
                self.length = min(int(length), general_vals.maxValidLength)
            case _:
                self.err_number_of_arguments(len(args), 2)
                return
        self.persist = persist
        self.run()
        return

    def run(self) -> None:
        """
        Send the read request to the server

        -> read file
        -> beginning at offset
        -> for a length of length bytes
        -> data is requested while the response is kXR_oksofar, ends
        as soon as any other response is received

        o also includes extended validation using check_response_ok
        o also check whether the file is in the filetable
        """
        logging.debug(f"Beginning read with offset={self.offset} length={self.length}")

        if not self.persist.ft_entry_exists(self.path):
            # Checking if it is not yet open
            logging.warning("Aborting read process.") 
            return

        args = (
            request_codes.kXR_read,
            self.persist.filetable[self.path].to_bytes(4, 'big'),
            self.offset,
            self.length,
            0, # no arguments -> alen = 0 TODO fix this
        )
        send(
            self.socket,
            f"!H4sqll",
            args,
        )


        reqcode = request_codes.kXR_oksofar
        while reqcode == request_codes.kXR_oksofar:
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
            dlen = unpack("!l", self.socket.recv(4))[0]
            data = unpack(f"!{dlen}s", self.socket.recv(dlen))[0]
            logging.debug(f"dlen={dlen}")
            print(data)

        logging.info("Read completed.")
        return

