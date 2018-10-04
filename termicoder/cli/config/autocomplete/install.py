import click
from . import click_completion
from ....utils.logging import logger


@click.command()
@click.option('--append/--overwrite',
              help="Append the completion code to the file", default=None)
@click.option('-i', '--case-insensitive/--no-case-insensitive',
              help="Case insensitive completion")
@click.argument('shell', required=False,
                type=click_completion.DocumentedChoice(
                    click_completion.core.shells))
@click.argument('path', required=False)
def main(append, case_insensitive, shell, path):
    """Install the click-completion-command completion"""
    if case_insensitive:
        extra_env = {
            '_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'
        }
    else:
        extra_env = {}
    shell, path = click_completion.core.install(
        shell=shell, path=path, append=append, extra_env=extra_env)
    logger.info('%s completion installed in %s' % (shell, path))
