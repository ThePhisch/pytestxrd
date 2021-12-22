import argparse

def cli_args() -> tuple[str, int]:
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", type=str, help="the host")
    parser.add_argument(
        "port", type=int, nargs="?", default=1094, help="port number, default"
    )
    args = parser.parse_args()
    return (args.hostname, args.port)