from os import stat
import socket
from functions.function_baseclass import Pytestxrd_Base_Function

class Dir(Pytestxrd_Base_Function):

    @staticmethod
    def help_str() -> str:
        return "dir\t[c] [o] [s] <path>\n\twhere: c->chksum o->online s->return stat"

    def __init__(self, args: list[str], socket: socket.socket) -> None:
        super().__init__(socket)