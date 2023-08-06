import argparse
from ._typing import Command

COMMANDS = [
    Command("create-app", "Create a new project."),
    Command("list", "List all your projects."),
    Command("setup", "Save API token.", param="token", param_help="Store API token", param_type=str),
]


def parse_args():
    parser = argparse.ArgumentParser(description="HEPIA project manager.")

    subparsers = parser.add_subparsers(help="Custom commands", dest="command")

    for c in COMMANDS:
        tmp_parser = subparsers.add_parser(c.name, help=c.help)
        if c.param != "":
            tmp_parser.add_argument(f"--{c.param}", help=c.param_help, type=c.param_type, required=c.param_required)

    args = parser.parse_args()

    args_values = vars(args)
    if not any(args_values.values()):
        parser.error("No commands provided.")

    return args
