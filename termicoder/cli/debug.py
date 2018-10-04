import click
from ..utils.logging import logger
from ..utils.exceptions import handle_exceptions


@click.command()
@handle_exceptions(BaseException)
def main():
    '''
    Launches custom debug interface.
    Here you can use testcase generator,
    launch debugger for the particular language
    and visualize the output.

    NOTE:
    This functionality is not implemented in this version.
    This option is only included for compatibility purposes.
    If you want to contribute to its development visit:
    https://termicoder.github.io/
    '''
    logger.info(
        'This functionality is not implemented in this version\n' +
        'The command is only kept for compatibility with future versions\n' +
        'If you want to contribute to its development visit:\n' +
        'https://termicoder.github.io/')
