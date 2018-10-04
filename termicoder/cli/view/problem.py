import click
from ...models import JudgeFactory
from ...utils.constants import default_judge
from ...utils.logging import logger
from ...utils.exceptions import handle_exceptions
from ...utils.launch import launch, substitute
from ...utils import config


judge_factory = JudgeFactory()
OJs = judge_factory.available_judges


@click.command(short_help="View a particular problem")
@click.option('-j', '--judge', 'judge_name', type=click.Choice(OJs),
              prompt="Please provide a judge("+'|'.join(OJs)+")",
              default=default_judge)
@click.option('-c', '--contest', type=click.STRING, help="contest code")
@click.option("--browser", help='Browser to launch',
              default=config.read('settings.yml', 'browser_online'))
@click.argument('PROBLEM_CODE')
@handle_exceptions(BaseException)
def main(judge_name, contest, problem_code, browser):
    '''
    View a particular problem from the judge.
    '''
    judge = judge_factory.get_judge(judge_name)
    problem_url = judge.get_problem_url(problem_code=problem_code,
                                        contest_code=contest)
    logger.debug('launching %s' % problem_url)
    keymap = {
        'URL': problem_url
    }
    status, browser = substitute(browser, keymap)
    if status is True:
        problem_url = ''
    launch(browser, problem_url)
