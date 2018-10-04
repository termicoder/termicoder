import click
from ...models import JudgeFactory
from ...utils.constants import default_judge
from ...utils.logging import logger
from ...utils.exceptions import handle_exceptions

judge_factory = JudgeFactory()
OJs = judge_factory.available_judges


@click.command()
@click.option('-j', '--judge', 'judge_name', type=click.Choice(OJs),
              prompt="Please provide a judge ("+'|'.join(OJs)+")",
              default=default_judge, show_default=True)
@handle_exceptions(BaseException)
def main(judge_name):
    '''
    View all running contests.
    '''

    # TODO judge.check_login and print current status
    judge = judge_factory.get_judge(judge_name)
    running_contests = judge.get_running_contests()
    click.echo_via_pager(running_contests)
