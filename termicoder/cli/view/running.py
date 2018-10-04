import click
from ...models import JudgeFactory
from ...utils.constants import default_judge
from ...utils.exceptions import handle_exceptions
from ...utils import config
from ...utils.launch import launch, substitute

judge_factory = JudgeFactory()
OJs = judge_factory.available_judges


@click.command()
@click.option('-j', '--judge', 'judge_name', type=click.Choice(OJs),
              prompt="Please provide a judge ("+'|'.join(OJs)+")",
              default=default_judge, show_default=True)
@click.option("--browser", help='Browser to launch',
              default=config.read('settings.yml', 'browser_online'))
@handle_exceptions(BaseException)
def main(judge_name, browser):
    '''
    View all running contests.
    '''

    judge = judge_factory.get_judge(judge_name)
    contest_list_url = judge.get_contests_list_url()
    keymap = {
        'URL': contest_list_url
    }
    status, browser = substitute(browser, keymap)
    if status is True:
        contest_url = ''
    launch(browser, contest_url)
