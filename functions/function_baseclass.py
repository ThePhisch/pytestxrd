import socket


class Pytestxrd_Base_Function():

    @classmethod
    def help_str(cls) -> str:
        return "Help has not been defined for this function."

    def __init__(self, socket: socket.socket) -> None:
        self.socket = socket

    def run(self) -> None:
        pass