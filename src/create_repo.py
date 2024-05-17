"""

This script in on charge to handle the creation of a new repo


"""
import os
from tools.debug import debug


def init() -> None:
    """Init repo"""
    path = os.getcwd()  # get path
    if os.system(f"git -C {path} init >/dev/null") == 0:
        debug("repositorie created!!", "M")
    else:
        debug("fatal error couldn't create repositorie", "E")


init()
