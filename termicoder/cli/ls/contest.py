import click
from ...models import JudgeFactory
from ...utils.constants import default_judge
from ...utils.logging import logger
from ...utils.exceptions import handle_exceptions

judge_factory = JudgeFactory()
OJs = judge_factory.available_judges
if default_judge is None:
    try:
        default_judge = OJs[0]
    except IndexError:
        pass


@click.command(short_help="List a particular contest.")
@click.option('-j', '--judge', type=click.Choice(OJs),
              # prompt="Please provide a judge("+'|'.join(OJs)+")",
              default=default_judge)
@handle_exceptions(BaseException)
def main(judge):
    '''
    List problems from a particular contest with their status.

    depending on judge it may give a list of categories also
    such as PRACTICE etc.
    '''
    logger.error('Not implemented list contest in this version')
    return
