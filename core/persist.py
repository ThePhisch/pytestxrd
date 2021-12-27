import logging


class Persist:
    """
    Class to run globally (called in pytestxrd) and persistently
    store

    o the files that have been opened during the session
    o the history of human inputs
    """

    def __init__(self):
        logging.debug("Initialising an empty FileTable")
        self.filetable: dict[str, int] = {}

    def ft_add_entry(self, path_name: str, fhandle: int) -> None:
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

    def ft_remove_entry(self, path_name: str) -> None:
        del self.filetable[path_name]
        logging.debug(f"File '{path_name}' has been removed from filetable")
        return

    def ft_entry_exists(self, path_name: str) -> bool:
        is_in: bool = path_name in self.filetable
        if is_in:
            logging.warning(f"File '{path_name}' is aleady open")
        else:
            logging.debug(f"File '{path_name}' is not open yet")
        return is_in
