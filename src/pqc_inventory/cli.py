"""Command-line entry point with structured output and sanitized errors."""

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from pqc_inventory import __version__
from pqc_inventory.directory_scanner import scan_directory
from pqc_inventory.tls_scanner import ScanError, scan_tls


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pqc-scan", description="PQC Crypto Inventory Lab"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command")
    tls = commands.add_parser("tls", help="One verified TLS handshake")
    tls.add_argument("host")
    tls.add_argument("--port", type=int, default=443)
    tls.add_argument("--timeout", type=float, default=5.0)
    directory = commands.add_parser("directory", help="Inventory an explicitly chosen directory")
    directory.add_argument("path", type=Path)
    directory.add_argument("--max-files", type=int, default=10000)
    args = parser.parse_args(argv)
    try:
        if args.command == "tls":
            print(json.dumps(scan_tls(args.host, args.port, args.timeout), indent=2))
        elif args.command == "directory":
            print(json.dumps(scan_directory(args.path, args.max_files), indent=2))
        else:
            parser.print_help()
    except ScanError as error:
        print(json.dumps({"event": "scan_failed", "error": str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
