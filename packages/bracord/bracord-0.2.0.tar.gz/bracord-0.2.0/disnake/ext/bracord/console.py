"""
This file is responsible for handling the CLI.
"""

import argparse
from disnake.ext.bracord.console_commands import cog, init_project

command_options = ["init", "cog"]

parser = argparse.ArgumentParser(
    prog="bracord",
    description="A Disnake framework written in Python that speeds the development of Discord bots.",
    add_help=True,
)

parser.add_argument(
    "command",
    help="The command you want to run.",
    choices=command_options,
)


def main():
    """Main Function that will run whenever the command "bracord" is called."""
    args = parser.parse_args()

    if args.command == "cog":
        cog()

    if args.command == "init":
        init_project()
