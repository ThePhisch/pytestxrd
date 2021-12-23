import socket
from struct import pack
from definitions import general_vals, request_codes
from functions.function_baseclass import Pytestxrd_Base_Function

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
                print(f"This will work out. {oldp} -> {newp}")
                self.oldp = oldp
                self.newp = newp + "X" # to counteract truncation
                self.run()
            case _:
                print(f"Check number of arguments: {len(args)}/2 args given")

    def run(self) -> None:
        plen = len(self.oldp + self.newp)
        self.socket.sendall(
            pack(
                f"!HH14sHl{plen}s",
                general_vals.StreamID,
                request_codes.kXR_mv,
                b"\0"*14,
                len(self.oldp),
                plen,
                f"{self.oldp} {self.newp}".encode("UTF-8")
            )
        ) # type: ignore