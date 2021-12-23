import socket
from functions.function_baseclass import Pytestxrd_Base_Function

class Testfunc(Pytestxrd_Base_Function):

    @classmethod
    def help_str(cls) -> str:
        return "testfunc"

    def __init__(self, args: list[str], socket: socket.socket) -> None:
        super().__init__(socket)