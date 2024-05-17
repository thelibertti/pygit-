"""

debug code easily


"""
from colorama import Fore


def debug(message: str, type_of_information: str) -> None:
    """
    debug/print useful information into de console
    nicer and esier

    types of information and their color:
    "I", (information):GREEN
    "M", (message):BLUE
    "W", (warning):YELLOW
    "E", (error): RED
    """

    types_info = {
        "I": [Fore.GREEN, "[INFO] "],
        "M": [Fore.BLUE, "[MSG] "],
        "W": [Fore.YELLOW, "[WARN] "],
        "E": [Fore.RED, "[ERROR] "]  # NOTE: dont forget to add the space
    }

    if type_of_information in types_info:
        info_selected = types_info[type_of_information]
        msg = info_selected[0] + info_selected[1] + message
        print(f"{msg} {Fore.RESET}")
    else:
        print(Fore.GREEN + "[I] " + message + Fore.RESET)
