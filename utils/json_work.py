"""
Module to work with json files
"""
import json
import os
from .debug import print_cf
from .debug import debug
from .tools import yes_or_no_menu

confi_path = os.path.expanduser("~/.pygit/pygitconf.json")


def write_into_json_file(data: str) -> None:
    """
    Writes the provided data into the 'pygitconf.json'
    file

    Raises FileNotFoundError in case confi hasn't been set
    """

    data = data.strip()
    try:
        with open(confi_path, "a") as file:

            file.write(data)
            file.close()

    except FileNotFoundError:
        debug("Not configura was found", "E")
        exit(1)


def write_new_profile(profile_data: dict[str: str]) -> None:
    """
    Writes a new profile into
    '.pygitconfig.json'
    """

    path = os.path.expanduser("~/.pygit/pygitconf.json")

    name = profile_data['name']
    email = profile_data['email']
    branch = profile_data['branch']
    msg = profile_data['commit_msg']

    profile_body = {
        "email": email,
        "branch": branch,
        "msg": msg
    }

    with open(path, 'r') as f:
        content = json.loads(f.read())
        f.close()

    content['profiles'][name] = profile_body
    with open(path, 'w') as f:
        json.dump(content, f, indent=4)
        f.close()
