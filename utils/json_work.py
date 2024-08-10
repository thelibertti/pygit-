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


def get_information() -> dict[str: str]:
    while True:
        print_cf("Hey welcome lets setup your profile!", "C", "B")

        print()
        print_cf("What will be your username", "C")
        usr_name = input("> ")

        print()
        print_cf("What will be your email?", "C")
        usr_email = input("> ")

        print()
        print_cf("what will be your default branch", "C")
        usr_branch = input("> ")

        os.system("clear")

        print_cf("Is this information current?")
        print()
        debug("User Name:", "I")
        print(usr_name)

        print()
        debug("User Email:", "I")
        print(usr_email)

        print()
        debug("Default Branch:", "I")
        print(usr_branch)

        if yes_or_no_menu() == "Y":
            info = {
                "name": usr_name,
                "email": usr_email,
                "branch": usr_branch
            }
            break
            return info

        continue


def add_new_profile(email):
    info = get_information()
    with open("~/pygitconf.json", "") as f:
        raise NotImplementedError
