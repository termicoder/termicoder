import click
from ...utils.exceptions import handle_exceptions
from ...utils import view
from ...utils import config


@click.command(short_help="View contents of folder.")
@click.argument("dir_name", type=click.Path(
                    exists=True, file_okay=False, dir_okay=True), default='.')
@click.option("--browser", help='Browser to launch',
              default=config.read('settings.yml', 'browser_local'))
@handle_exceptions(BaseException)
def main(dir_name, browser):
    '''
    display the termicoder contents in current/passed folder

    \b
    if it is a contest folder it displays the list of problems.
    if its a problem folder, displays the problem in a browser.
    '''
    view.folder(dir_name, browser)
