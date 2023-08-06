import requests
import os
import json
from typing import List
from rich.console import Console
from ._typing import Group, Project

BASE_URI = "https://gitedu.hesge.ch/api/v4"
console = Console()

try:
    token = open("./config.txt", "r").read()
except Exception as e:
    token = ""


def get_owned_groups() -> List[Group]:
    """Get user owned groups

    Returns:
        Group[]: List of owned groups
    """
    if token == "":
        print("No token as been register. Please do so using `setup --token <TOKEN_VALUE>.`")
        return None

    url = f'{BASE_URI}/groups?owned=true&per_page=100'

    payload = {}
    headers = {
        'Private-Token': token
    }

    with console.status("[bold green]Getting groups...") as status:
        response = requests.request("GET", url, headers=headers, data=payload).text
    response = json.loads(response)

    groups: List[Group] = []
    # @see: https://gitedu.hesge.ch/help/api/groups.md#list-groups
    for g in response:
        groups.append(Group(g['id'], g['name'], g['path'], g['description'],
                      g['visibility'], g['web_url'], g['full_path'], g['parent_id']))

    return groups


def get_owned_projects(page=1):
    """Get user owned projects

    Return:
        Project[]: List of owned projects
    """
    if token == "":
        print("No token as been register. Please do so using `setup --token <TOKEN_VALUE>.`")
        return None

    url = f'{BASE_URI}/projects?membership=true&page={page}'

    payload = {}
    headers = {
        'Private-Token': token
    }

    with console.status("[bold green]Getting projects...") as status:
        response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text)

    p_list: List[Project] = []
    # @see: https://gitedu.hesge.ch/help/api/projects.md#list-all-projects
    for p in response_json:
        p_list.append(Project(p['id'], p['description'], p['web_url'], p['name'],
                              p['path_with_namespace'], p['star_count'], p['open_issues_count'], p['namespace']['id'], p['namespace']['name']))

    return {
        # @see: https://stackoverflow.com/a/45087988 for informations on headers
        'headers': {
            'X-Next-Page': response.headers.get('X-Next-Page'),
            'X-Prev-Page': response.headers.get('X-Prev-Page'),
            'X-Total-Pages': response.headers.get('X-Total-Pages'),
        },
        # Sort the project by full namespace for easier print later
        'list': sorted(p_list, key=lambda k: k.path_with_namespace)
    }
