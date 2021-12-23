import argparse
import logging


def cli_args() -> tuple[str, int]:
    """
    Setup the parsing of arguments
    : Hostname
    : Port (optional) (positional) default 1094
    : debug levels (optional) options 0,1,2
    -> passes hostname and port as tuple
    -> calls the setup_logging() function with the logging level
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", type=str, help="the host")
    parser.add_argument(
        "port", type=int, nargs="?", default=1094, help="port number, default"
    )
    parser.add_argument(
        "--debug",
        "-d",
        help="toggle debug mode (increased verbosity)",
        type=int,
        choices=[0, 1, 2],
        default=0,
    )
    args = parser.parse_args()
    setup_logging(args.debug)
    return (args.hostname, args.port)


def setup_logging(chosen_level: int) -> None:
    """
    Sets up logging depending on the chosen log level
    : chosen_level
    -> minimum level for log to become visible: 0 warning; 1 info; 2 debug
    """
    match chosen_level:
        case 0:
            logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s:%(message)s")
            logging.debug("Logging remains at WARNING")
        case 1:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")
            logging.info("Logging has been set to INFO")
        case 2:
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(message)s")
            logging.info("Logging has been set to DEBUG")