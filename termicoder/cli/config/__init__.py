import click
from . import autocomplete
from . import init
from . import man
from . import edit
from . import remove


@click.group()
def main():
    """
    Configure settings, autocomplete etc.
    """
#    raise NotImplementedError
#    eval(judge).setup(contest, problem, status)


sub_commands = [
    {
        "cmd": autocomplete.main,
        "name": "autocomplete"
    },
    {
        "cmd": init.main,
        "name": "init"
    },
    {
        "cmd": man.main,
        "name": "man"
    },
    {
        "cmd": edit.main,
        "name": "edit"
    },
    {
        "cmd": remove.main,
        "name": "remove"
    }
]

for command in sub_commands:
    main.add_command(**command)

__all__ = ['main']
