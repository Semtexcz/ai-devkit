"""Entry point for the example script.

The greeting is customizable: `python main.py --name Ada` greets Ada, while running
without arguments prints the greeting the scaffold produced.
"""

from __future__ import annotations

import argparse

DEFAULT_NAME = "script-project"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Return the parsed command line."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument(
        "--name",
        default=DEFAULT_NAME,
        help=f"name to greet (default: {DEFAULT_NAME})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Print the greeting."""
    args = parse_args(argv)
    print(f"Hello from {args.name}!")


if __name__ == "__main__":
    main()
