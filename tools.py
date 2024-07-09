"""
Module Tools:

A bunch of tools usefull for the develoment
of pigit++

"""
from simple_term_menu import TerminalMenu
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.buffer import Buffer


def multiple_choice_menu(options: list, title=None) -> int:
    """
    displays a multiple choice menu into the terminal

    NOTE: this funtion returns the index of the option
    picked.

    """
    menu = TerminalMenu(options,
                        title=title,
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


def multiple_selection_menu(options: list, title="") -> list:
    """
    Multiple option menu that lets the user pick
    multiple options

    Note: this funtion will return a list with the index of the
    options the user picks

    """
    menu = TerminalMenu(
        options,
        title=title,
        menu_highlight_style=('fg_cyan', 'bg_black'),
        multi_select=True,
        show_multi_select_hint=True,
        preview_command="bat --color=always {}", preview_size=0.75)

    index = menu.show()
    return index


class miniCommitTypingApp:
    """
    The app tha handles the write of the commit
    """

    def __init__(self, preffix: str):
        self.counter = 0
        self.msg = FormattedTextControl(
            lambda: "Please write your commit message "
        )
        self.preffix_info = FormattedTextControl(
            lambda: f"Preffix: {preffix}"
        )
        self.text_leng_commit = FormattedTextControl(
            lambda: f"Commit Leng: {self.counter}"
        )

        self.bidings = KeyBindings()
        self.bidings.add('<any>')(self.count_key)
        self.bidings.add('backspace')(self.handle_backspace)
        self.bidings.add('enter')(self.handle_enter)

        self.buffer = Buffer(
            multiline=True
        )

        self.container = HSplit([

            VSplit([
                Window(
                    content=self.msg,
                    height=1,
                    dont_extend_height=True,
                    style="fg:cyan"
                ),
                Window(
                    content=self.preffix_info,
                    height=1,
                    dont_extend_height=True,
                    style="fg:yellow"
                ),
                Window(
                    content=self.text_leng_commit,
                    height=1,
                    dont_extend_height=True,
                    style=self.get_color_code
                )
            ]),
            VSplit([
                Window(
                    content=FormattedTextControl(">> "),
                    width=3, dont_extend_width=True
                ),
                Window(
                    content=BufferControl(buffer=self.buffer)
                )
            ])
        ])

        self.app = Application(
            layout=Layout(self.container),
            key_bindings=self.bidings
        )

    def count_key(self, event):
        self.counter += 1
        data = event.data
        self.buffer.insert_text(data=data)
        self.app.invalidate()

    def handle_backspace(self, event):
        if self.counter != 0:
            self.counter = self.counter - 1
        self.buffer.delete_before_cursor(1)

    def handle_enter(self, event):
        self.app.exit()

    def get_color_code(self) -> str:
        """
        Returns the color code based on the value of self.counter
        """
        if self.counter > 250:
            return 'fg:red'
        elif 125 < self.counter <= 250:
            return 'fg:yellow'
        elif 55 < self.counter <= 125:
            return 'fg:green'
        else:
            return 'fg:blue'

    async def run(self):
        await self.app.run_async()
        return self.buffer.text
