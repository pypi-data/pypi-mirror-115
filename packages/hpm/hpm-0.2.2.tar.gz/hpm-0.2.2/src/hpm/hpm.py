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
from rich.box import DOUBLE_EDGE
from . import args as arguments
from . import api
from dotenv import load_dotenv
import pathlib
from rich import align, print
from rich.panel import Panel
from rich.console import Group, Console
from rich.columns import Columns
from rich.text import Text
from .namespaces import create_namespace_tree
from ._printing import clr_scr, print_command_header, generate_project_tree, del_last_line
from .questions import QUESTIONS
from .errors import APIError

def main():
    # Append the .env file to the current symlink/file
    env_path = pathlib.Path(__file__).resolve().parent.absolute() / ".env"
    load_dotenv(dotenv_path=env_path)

    args = arguments.parse_args()
    console = Console()

    if args.command == "setup":
        if not args.token:
            print("Command `setup` require argument `--token`.")
            exit()
        
        with open(pathlib.Path(__file__).resolve().parent.absolute() / "config.txt", "w+") as f:
            f.write(args.token)
    elif args.command == "create-app":
        # @see: https://github.com/kefranabg/readme-md-generator for good cli use guidance
        print_command_header(args.command)

        for question in QUESTIONS:
            tmp_res = None
            prompt = f"[green]?[/green] [bright_white]{question.message}[/bright_white] "
            default_indication = f"[dim italic]({question.default})[/dim italic] "
            
            if question.default != "":
                prompt += default_indication
            
            # Prompt the question
            tmp_res = console.input(prompt)

            # Set the default value as current value when no provided
            if question.default != "" and tmp_res == "":
                prompt = prompt.replace(default_indication, "")
                tmp_res = question.default

            # Validate the user input
            while not question.set_response(tmp_res):
                del_last_line()
                tmp_res = console.input(f"{prompt}[red1]({question.help})[/red1] ")

            # Remove default indication prompt when entered a valid input
            if tmp_res != "":
                prompt = prompt.replace(default_indication, "")

            del_last_line()
            print(f"{prompt}[cyan]{question.response}[/cyan]")

            # Transform the response if needed for the api
            if question.transform != None:
                question.transform_response(tmp_res)
        
        # Create the api params list
        api_params = []
        for q in QUESTIONS:
            api_params.append({
                "key": q.name,
                "value": q.response
            })
        
        try:
            new_project = api.create_project(api_params)

            print("✅ Project created")
            print()
            print(f"👀 View the created project on [link {new_project.web_url}]{new_project.web_url}!")
            print()
            print(Panel(Text("Project was successfully created.\nThanks for using hpm !", justify="center"), box=DOUBLE_EDGE, border_style="bright_cyan", padding=(1, 2), expand=False))
            print()
        except APIError as e:
            print(e.message)
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

if __name__ == "__main__":
    main()