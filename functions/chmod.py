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
        return "chmod <mode> <path>"

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
        target_mode = self.get_mode(self.mode)
        if not target_mode:
            logging.warning(f"Bad target mode: {target_mode} aquired (likely due to error), aborting chmod")
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


    def get_mode(self, mode_str: str) -> int:
        """
        Get mode which will be passed to xrootd in the chmod request

        -> According to the protocol, the mode must be an 'or'd' combination
        of kXR_ur, _gr, _or, _uw and _gw.
        -> This leaves a number of combinations, which are checked out here.
        For user/group/other, the flags are determined and added to a list
        -> The list is then reduced by repeatedly applying bitwise OR
        """
        try:
            mode_intlist = list(map(lambda x: int(x), list(mode_str)))
        except ValueError:
            logging.warning("Converion from string to int array was not successful")
            return -1
        # throw error if it doesnt have length 3
        if len(mode_intlist) != 3:
            print(f"Check number of arguments in mode: {len(mode_intlist)} != 3")
            return -1
        mode_flaglist: list[int] = [0, 0] # seeded with two 0s so that the reduce wont fail in the end
        match mode_intlist[0]:
            case 2:
                mode_flaglist.append(request_codes.kXR_uw)
            case 4:
                mode_flaglist.append(request_codes.kXR_ur)
            case 6:
                mode_flaglist.append(request_codes.kXR_uw)
                mode_flaglist.append(request_codes.kXR_ur)
            case 0:
                pass
            case x:
                logging.warning(f"'User' Mode component: {x} not understood, revert to 0")
        match mode_intlist[1]:
            case 2:
                mode_flaglist.append(request_codes.kXR_gw)
            case 4:
                mode_flaglist.append(request_codes.kXR_gr)
            case 6:
                mode_flaglist.append(request_codes.kXR_gw)
                mode_flaglist.append(request_codes.kXR_gr)
            case 0:
                pass
            case x:
                logging.warning(f"'Group' Mode component: {x} not understood, revert to 0")
        match mode_intlist[2]:
            case 4:
                mode_flaglist.append(request_codes.kXR_or)
            case 0:
                pass
            case x:
                logging.warning(f"'Others' Mode component: {x} not understood, revert to 0")
        ordflags: int = reduce(lambda x,y: x | y, mode_flaglist)
        return ordflags
        # Question: is 000 a sane default???