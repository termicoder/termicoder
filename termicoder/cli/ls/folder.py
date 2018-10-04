import click
from ...utils.logging import logger
from ...utils.exceptions import handle_exceptions
from ...utils.load import get_problem_or_contest
from ...models import Problem, Contest
import subprocess


@click.command(short_help="View contents of folder.")
@click.argument("FOLDER", type=click.Path(
                    exists=True, file_okay=False, dir_okay=True), default='.')
@handle_exceptions(BaseException)
def main(folder):
    '''
    display the termicoder contents in current/passed folder

    \b
    if it is a contest folder it displays the list of problems.
    if its a problem folder, displays the problem in a browser.
    '''
    logger.warn('Dummy list in this version')
    p_or_c = get_problem_or_contest(folder)
    assert(isinstance(p_or_c, Problem) or isinstance(p_or_c, Contest))
    if(p_or_c is None):
        logger.warn('no .problem or .contest in current folder, running ls -l')
        subprocess.run(['ls', '-l', folder])
    else:
        click.echo_via_pager(str(p_or_c))
