import click
from ..utils.exceptions import handle_exceptions
from ..models import JudgeFactory
from ..utils import test as test_util
judge_factory = JudgeFactory()


@click.command()
@click.argument('code_file', type=click.Path(exists=True, dir_okay=False),
                required=False)
@click.option('-tl', '--timelimit', type=float,
              help="the max time per testcase")
@click.option('-l', '--live', is_flag=True, default=False,
              help="test the code live and don't use testcases")
@handle_exceptions(BaseException)
def main(code_file, timelimit, live):
    '''
    Test code against the sample testcases.

    \b
    this command (compiles and) runs passed code file.
    the code is run against all [.in] files in ./testcases folder.
    the output is produced in [.out] files and checked against [.ans] files

    it displays time for each testcase,status
    and diff of expected and produced outputs.
    '''
    test_util.test(code_file, timelimit, live, judge_factory)
