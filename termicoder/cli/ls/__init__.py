import click
from click_default_group import DefaultGroup

from . import contest
from . import folder
from . import running
from ...utils.logging import logger
from ...utils.exceptions import handle_exceptions


# view command has various subcommands
# default is termicoder view this
# TODO change default_if_no_args to true
@click.group(cls=DefaultGroup, default='folder', default_if_no_args=True)
@handle_exceptions(BaseException)
def main():
    '''
    List the contents of current folder.
    '''
    pass


sub_commands = [
    {
        "cmd": contest.main,
        "name": "contest"
    },
    {
        "cmd": folder.main,
        "name": "folder"
    },
    {
        "cmd": running.main,
        "name": "running"
    }
]


for command in sub_commands:
    main.add_command(**command)

__all__ = ['main']
