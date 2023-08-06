#!/usr/bin/python
"""hmp - HEPIA project manager

This script is a helper for all students at HEPIA
to assist the creation of a new coding project with
a gitlab (https://gitedu.hesge.ch) repo directly link
to the local instance.

@author : Tanguy Cavagna <tanguy.cvgn@ik.me>
@copyrigth : Copyright 2021, hpm
@version : 0.1
@status : developpement
"""

from typing import Text
import args as arguments
import api
from dotenv import load_dotenv
import pathlib
from rich import print
from rich.panel import Panel
from rich.console import Group, Console
from rich.columns import Columns
from rich.text import Text
from namespaces import create_namespace_tree
from _printing import clr_scr, print_command_header, generate_project_tree

def script():
    # Append the .env file to the current symlink/file
    env_path = pathlib.Path(__file__).resolve().parent.absolute() / ".env"
    load_dotenv(dotenv_path=env_path)

    args = arguments.parse_args()
    console = Console()

    if args.command == "setup":
        if not args.token:
            print("Command `setup` require argument `--token`.")
            exit()
        
        with open("./config.txt", "w+") as f:
            f.write(args.token)
    elif args.command == "create-app":
        clr_scr()
        print_command_header(args.command)
    elif args.command == "list":
        page = 1
        prev_page = 0
        co = ""

        # Emulate a `do {...} while()`
        while True:
            clr_scr()
            print_command_header(args.command)

            # Only call the api if the pages have changed
            if prev_page != page:
                groups = api.get_owned_groups()
                owned_projects = api.get_owned_projects(page)

                if groups is None or owned_projects is None:
                    exit()

                groups = sorted(groups, key=lambda k: k.full_path)
                headers = owned_projects["headers"]
                group_projects = owned_projects["list"]

            prev_page = "<" if (headers["X-Prev-Page"] != "") else ""
            next_page = ">" if (headers["X-Next-Page"] != "") else ""

            roots = []
            for root in create_namespace_tree(groups, group_projects):
                roots.append(Panel(generate_project_tree(root)))

            # Format navigation menu
            navigation = Group(
                Panel(
                    Group(
                        Text.assemble(
                            ("Page", "bright_white"),
                            f": {prev_page} ",
                            (str(page), "bright_white"),
                            "/",
                            (headers["X-Total-Pages"], "bright_white"),
                            f" next_page",
                            justify="center",
                        ),
                        Text.assemble(
                            ("Navigation", "bright_white"),
                            ": Previous (",
                            ("p", "green"),
                            ") | Next (",
                            ("n", "green"),
                            ") | Close (",
                            ("c", "red1"),
                            ") | ",
                            justify="center",
                        ),
                    )
                )
            )

            # Print
            print(Columns(roots))
            print(navigation)

            co = console.input("[bold magenta]Action: [/bold magenta]")

            # List commands
            if co == "c":
                break
            elif co == "p":
                if headers["X-Prev-Page"] != "":
                    prev_page = page
                    page = headers["X-Prev-Page"]
            elif co == "n":
                if headers["X-Next-Page"] != "":
                    prev_page = page
                    page = headers["X-Next-Page"]
            else:
                prev_page = page
                continue

            # `do {...} while()` condition
            if co == "c":
                break
    # Exit when command unknown
    else:
        exit()
