import os
import platform
from datetime import datetime
from rich import print
from rich.tree import Tree
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text


def generate_project_tree(namespace: dict, tree: Tree = None) -> None:
    """Print the project list

    Args:
        namespace (dict): Current namespace
        tree (Tree): Tree to build
    """
    if tree is None:
        tree = Tree(
            f'[link {namespace["url"]}][bold cyan]{namespace["name"]}[/bold cyan][/link {namespace["url"]}]'
        )
    else:
        tree = tree.add(
            f'[link {namespace["url"]}][bold cyan]{namespace["name"]}[/bold cyan][/link {namespace["url"]}]'
        )

    # Recursivly print the children
    for c in namespace["children"]:
        generate_project_tree(c, tree=tree)

    # Print the projects list
    for i, p in enumerate(namespace["projects"]):
        tree.add(
            f"{p.name} :glowing_star:{p.star_count} :name_badge:{p.open_issues_count}"
        )

    return tree


def print_command_header(command: str):
    """Global header

    Args:
        command (str): Executed command
    """
    print(
        Panel(
            Columns(
                [
                    Text("Made By Tanguy Cavagna with 💖", style="italic"),
                    Text(
                        datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
                        justify="right",
                        style="italic",
                    ),
                ],
                expand=True,
                title="[bold bright_white]HES-SO[/bold bright_white] - [bold red1]HEPIA[/bold red1]",
            ),
            border_style="bright_white",
            title=f"Command: [orange_red1]{command}[/orange_red1]",
            title_align="left",
        )
    )


def clr_scr():
    """Clear screen on all os"""
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")
