import click
from ..utils.logging import logger
from ..utils.exceptions import handle_exceptions
from ..models import JudgeFactory
from ..utils import yaml
from ..utils.load import get_default_code_name
import os

judge_factory = JudgeFactory()


@click.command()
@click.argument('code_file', type=click.Path(exists=True, dir_okay=False),
                required=False)
@handle_exceptions(BaseException)
def main(code_file):
    '''
    Submit a solution.

    You should be in a problem directory to submit

    \b
    Script will prompt you to login into the judge(if not already).
    '''
    if '.problem.yml' not in os.listdir():
        logger.error("You should be in a problem directory to submit")
        return

    if(code_file is None):
        default_file = get_default_code_name()
        if (not os.path.exists(default_file)):
            default_file = None
        code_file = click.prompt(
            "Please a code file to submit",
            default=default_file,
            type=click.Path(readable=True, exists=True)
        )

    code = click.open_file(code_file).read()
    extension = code_file.split(".")[-1]
    problem = yaml.read('.problem.yml')
    judge = judge_factory.get_judge(problem.judge_name)
    judge.submit(problem, code, extension)
