"""
Module Tools:

A bunch of tools useful for the develoment
of pigit++

"""
from simple_term_menu import TerminalMenu


def multiple_choice_menu(options: list) -> int:
    """
    displays a multiple choice menu into the terminal

    NOTE: this funtion returns the index of the option
    picked.

    """
    menu = TerminalMenu(options,
                        title="Please select a option:",
                        menu_highlight_style=("fg_cyan", "bg_black"))
    index = menu.show()
    return index


def yes_or_no_menu() -> str:
    """
    Displays a yes or not menu

    Note: This function will return 'Y' if the user
    picks yes or 'N' if the user picks no
    """
    options = ['yes', 'no']

    menu = TerminalMenu(options, menu_highlight_style=('fg_cyan', 'bg_black'))
    index = menu.show()
    if index == 0:
        return "Y"
    else:
        return "N"
