import logging
import socket
from definitions import general_vals, request_codes
from functions.function_baseclass import Pytestxrd_Base_Function
from core.connect import send
from functools import reduce

class Chmod(Pytestxrd_Base_Function):
    """
    Implements the chmod function
    """

    @staticmethod
    def help_str() -> str:
        return "chmod\t<mode> <path>"

    def __init__(self, args: list[str], socket: socket.socket) -> None:
        super().__init__(socket)
        match args:
            case [mode, path]:
                self.mode = mode
                self.path = path
                self.run()
            case _:
                print(f"Check number of arguments: {len(args)}/2 args given") # TODO move this to baseclass

    def run(self) -> None:
        """
        Chmod <file> with permissions <mode>
        """
        logging.debug(f"mode passed (as str) is {self.mode}")
        forbidden_flags = {
                request_codes.kXR_ow,
                request_codes.kXR_ux,
                request_codes.kXR_gx,
                request_codes.kXR_ox,
                }
        target_mode = self.get_mode(self.mode, forbidden_flags)
        if target_mode <= 0:
            logging.warning(f"Bad target mode: {target_mode} aquired (likely due to error), aborting chmod")
            return
        logging.debug(f"Or'd combination of flags results in target: {target_mode}")

        plen = len(self.path)
        args = (
            request_codes.kXR_chmod,
            b"\0"*14,
            target_mode,
            plen,
            self.path.encode("UTF-8"),
        )
        send(
            self.socket,
            f"!H14shl{plen}s",
            args,
        )
        if self.check_response_ok():
            logging.info("chmod succeeded.")


