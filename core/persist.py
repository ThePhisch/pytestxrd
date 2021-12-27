import logging

"""
This file stores classes that shall store information and make it
available globally (and persistently)
"""


class FileTable:
    """
    Class to run globally (called in pytestxrd) and persistently
    store the files that have been opened during the session

    -> essentially a wrapper for a dictionary, but who knows
    whether I need to extend this later
    """

    def __init__(self):
        logging.debug("Initialising an empty FileTable")
        self.filetable: dict[str, int] = {}

    def add_entry(self, path_name: str, fhandle: int) -> None:
        if path_name not in self.filetable:
            self.filetable[path_name] = fhandle
            logging.debug(
                f"File '{path_name}' with fhandle value {fhandle} has been entered into filetable"
            )
            return
        else:
            # this should never happen
            # that the file isnt already open should already be ascertained
            logging.warning(f"File '{path_name}' is already open, aborting")
            return

    def remove_entry(self, path_name: str) -> None:
        del self.filetable[path_name]
        logging.debug(f"File '{path_name}' has been removed from filetable")
        return

    def entry_does_not_exist(self, path_name: str) -> bool:
        is_in: bool = path_name in self.filetable
        if is_in:
            logging.warning(f"File '{path_name}' is aleady open")
        else:
            logging.debug(f"File '{path_name}' is not open yet")
        return not is_in
