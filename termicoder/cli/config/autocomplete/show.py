import click
from . import click_completion


@click.command()
@click.option('-i', '--case-insensitive/--no-case-insensitive',
              help="Case insensitive completion")
@click.argument('shell', required=False,
                type=click_completion.DocumentedChoice(
                    click_completion.core.shells))
def main(shell, case_insensitive):
    """Show the click-completion-command completion code"""
    if case_insensitive:
        extra_env = {
            '_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'
        }
    else:
        extra_env = {}
    click.echo(click_completion.core.get_code(shell, extra_env=extra_env))
