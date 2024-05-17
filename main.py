from src.tools.debug import debug
import os

# TODO: move 'check_git' into the do config module


def check_git() -> None:  # first lest check for git to be installed
    """Check for git to be installed
    if not installed ask the user to installed"""

    if os.system("command -v git >/dev/null") != 0:
        debug("git not found in this divice", "W")
        debug("install it with your device's packages manager", "I")
