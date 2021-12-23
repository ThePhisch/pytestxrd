import argparse


def cli_args() -> tuple[str, int, bool]:
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", type=str, help="the host")
    parser.add_argument(
        "port", type=int, nargs="?", default=1094, help="port number, default"
    )
    parser.add_argument(
        "--debug",
        "-d",
        help="toggle debug mode (increased verbosity)",
        action="store_true",
    )
    args = parser.parse_args()
    return (args.hostname, args.port, args.debug)
