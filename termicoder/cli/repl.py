import click
import os
from click_repl import repl
from prompt_toolkit.history import FileHistory
from ..utils.logging import logger
from ..utils.exceptions import handle_exceptions

@click.command()
def main():
    '''
    Start an interactive shell. All commands and subcommands are available
    in it.

    If stdin is not a TTY, no prompt will be printed, but only commands read
    from stdin.
    '''

    prompt_kwargs = {
        'history': FileHistory(os.path.expanduser('~/.termicoder-history')),
    }
    repl(click.get_current_context(), prompt_kwargs=prompt_kwargs)
