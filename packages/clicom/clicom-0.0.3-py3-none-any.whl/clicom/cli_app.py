import sys
from typing import Optional

import typer


class ExitCommand(SystemExit):
    pass


class CLIApp(typer.Typer):
    def __init__(self, *args, sign: Optional[str] = None, add_help_option: bool = True, **kwargs):
        super().__init__(*args, add_help_option=add_help_option, **kwargs)
        self.sign = sign or ">"

        @self.command(name="exit", help="Exits current shell.")
        def exit_command():
            raise ExitCommand

        @self.command(name="help", help="Show help.", add_help_option=False)
        def help_command():
            if add_help_option:
                sys.argv = [sys.argv[0], "--help", *sys.argv[1:]]
                self()

    def _call_app_wrapper(self, get_input: bool = False):
        try:
            if get_input:
                i = input(self.sign + " ")
                if i == '':
                    return
                sys.argv = [sys.argv[0], *i.split(sep=" ")]
            self()
        except (KeyboardInterrupt, ExitCommand):
            exit(0)
        except BaseException:
            pass

    def start_app(self):
        self._call_app_wrapper(get_input=False)
        while True:
            self._call_app_wrapper(get_input=True)
