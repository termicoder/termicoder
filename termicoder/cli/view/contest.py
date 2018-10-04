import click
from ...models import JudgeFactory
from ...utils.constants import default_judge
from ...utils.logging import logger
from ...utils.exceptions import handle_exceptions
from ...utils import config
from ...utils.launch import launch, substitute

judge_factory = JudgeFactory()
OJs = judge_factory.available_judges


@click.command(short_help="Display a particular contest")
@click.option('-j', '--judge', 'judge_name', type=click.Choice(OJs),
              prompt="Please provide a judge("+'|'.join(OJs)+")",
              default=default_judge)
@click.option("--browser", help='Browser to launch',
              default=config.read('settings.yml', 'browser_online'))
@click.argument('CONTEST_CODE', required=False)
@handle_exceptions(BaseException)
def main(judge_name, contest_code, browser):
    '''
    View a contest from the judge (online).
    Launches the contest in browser.
    '''
    judge = judge_factory.get_judge(judge_name)
    contest_url = judge.get_contest_url(contest_code=contest_code)
    keymap = {
        "URL": contest_url
    }
    logger.debug('launching %s' % contest_url)
    status, browser = substitute(browser, keymap)
    if status is True:
        contest_url = ''
    launch(browser, contest_url)
