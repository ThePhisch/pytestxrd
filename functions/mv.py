import socket
from functions.function_baseclass import Pytestxrd_Base_Function

class Mv(Pytestxrd_Base_Function):

    @classmethod
    def help_str(cls) -> str:
        return "mv <old_path> <new_path>"

    def __init__(self, args: list[str], socket: type[socket.socket]) -> None:
        super().__init__(socket)
        match args:
            case [oldp, newp]:
                print(f"This will work out. {oldp} -> {newp}")
                self.oldp = oldp
                self.newp = newp
            case _:
                print(f"Check number of arguments: {len(args)}/2 args given")

    def run(self) -> None:
        pass