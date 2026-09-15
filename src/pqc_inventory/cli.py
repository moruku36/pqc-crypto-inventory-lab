"""Command-line entry point; scanners are introduced in subsequent phases."""

import argparse
from collections.abc import Sequence

from pqc_inventory import __version__


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pqc-scan", description="PQC Crypto Inventory Lab (Phase 0 scaffold)"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.parse_args(argv)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
