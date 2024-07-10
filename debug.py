"""
Module debug:

Useful to print colorful messages into
the console

"""
from colorama import Back
from colorama import Fore
from colorama import Style


def debug(message: str, type_message: str):
    message = str(message)
    """
    Usage:
    debug('foo', "I")

    will return:
    [Info] foo # in a green color

    avaiable types of messages are:

    "I", (information), color: green,
    "M", (message), color: blue
    "W", (warning), color: yellow
    "E", (error), color: red
    """

    colors = {
        'I': '\033[92m[INFO] ',
        'M': '\033[94m[MSG] ',
        'W': '\033[93m[WARN] ',
        'E': '\033[91m[ERROR] ',
        'reset': '\033[0m'
    }

    if type_message in colors:
        print(f"{colors[type_message]} {message} {colors["reset"]}")
    else:
        print(f"{colors["I"]} {message} {colors["reset"]}")


def print_cf(string: str, color: str, bg_color=None):
    string = str(string)
    """
    Print colorfull messages into the console,

    Usage:
    print_colorful("foo", "Y", "green")

    will print: foo (in a yellow color with a green background)

    avaible colors:
        - "Y" (yellow),
        - "B" (blue),
        - "G" (green),
        - "R" (red),
        - "M" (magenta)
        - "C" (cyan)

    NOTE: You can pass both the full name of the color or just the
    inital capital letter both will work

    Note: The default value for background color is None

    NOTE: If for example you dont want to have a background you can
    pass 'None' as argument
    """
    avaiable_colors = {
        ("green", "G"): (Fore.GREEN, Back.GREEN),
        ("yellow", "Y"): (Fore.YELLOW, Back.YELLOW),
        ("blue", "B"): (Fore.BLUE, Back.BLUE),
        ("red", "R"): (Fore.RED, Back.RED),
        ("magenta", "M"): (Fore.MAGENTA, Back.MAGENTA),
        ("cyan", "C"): (Fore.CYAN, Back.CYAN)
    }

    for key, value in avaiable_colors.items():
        if color == key[0] or color == key[1]:
            msg_color = value[0]
            break

        else:
            msg_color = Fore.WHITE

    for key, value in avaiable_colors.items():
        if bg_color == key[0] or bg_color == key[1]:
            msg_bg = value[1]
            break

        else:
            msg_bg = Fore.WHITE

    print(f"{msg_bg} {msg_color} {string} {Style.RESET_ALL}")
