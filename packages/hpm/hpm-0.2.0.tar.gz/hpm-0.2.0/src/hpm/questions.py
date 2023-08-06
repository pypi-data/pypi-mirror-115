from collections import defaultdict
from os import name
import re
from ._typing import ProjectQuestion
from .api import get_owned_groups


def get_namespace_id(namespace_name: str) -> int:
    """Get the namespace id to privide to the api

    Args:
        namespace_name (str): Namespace name

    Returns:
        int: Namespace id
    """
    GROUPS = get_owned_groups()

    _id = [group.id for group in GROUPS if group.full_path == namespace_name]

    if len(_id) > 0:
        return _id[0]
    else:
        return -1


QUESTIONS = [
    ProjectQuestion(
        message="💡 Project name",
        name="name",
        default="",
        help="The name cannot contains space",
        res_type=str,
        validate=lambda v: bool(re.search(r"^[\w\d\-\s]*$", v) and len(v) > 0),
    ),
    ProjectQuestion(
        message="📁 Project path (use empty value to skip)",
        name="path",
        default="",
        help="The name cannot contains space",
        res_type=str,
        validate=lambda v: bool(re.search(r"^[\w\d\-]*$", v)),
    ),
    ProjectQuestion(
        message="📄 Project description (use empty value to skip)",
        name="description",
        default="",
        help="The length cannot pass 255",
        res_type=str,
        validate=lambda v: bool(len(v) <= 255),
    ),
    ProjectQuestion(
        message="📖 Initialize project with a README (y, n)",
        name="initialize_with_readme",
        default="n",
        help="Choose between y, and n",
        res_type=str,
        validate=lambda v: bool(v in ["y", "n"]),
        transform=lambda v: True if v == "y" else False,
    ),
    ProjectQuestion(
        message="👀 Project visibility",
        name="visibility",
        default="public",
        help="Choose between public, internal, or private",
        res_type=str,
        validate=lambda v: bool(v in ["public", "internal", "private"]),
    ),
    ProjectQuestion(
        message="🗃️ Project namespace (<group>\[/<subgroup>, ...], use empty value to skip)",
        name="namespace_id",
        default="",
        help="",
        res_type=str,
        validate=lambda v: bool(re.search(r"(^$|^[\w\d.-\/]*$|)", v)),
        transform=lambda v: get_namespace_id(v) if v != "" else None,
    ),
]
