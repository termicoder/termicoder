from ..models import Problem
from ..models import Contest
from ..models import Testcase
from .logging import logger
from ..utils.yaml import write
from builtins import FileExistsError
import click
import os


def output_testcase(testcase, testcase_dir):
    try:
        assert isinstance(testcase, Testcase)
        directory_path = testcase_dir
        inp_path = os.path.join(
            directory_path, '%s.in' % testcase.code)
        ans_path = os.path.join(
            directory_path, '%s.ans' % testcase.code)
        logger.debug(inp_path)
        logger.debug(ans_path)
        os.makedirs(directory_path)
    except FileExistsError:
        pass
    except AssertionError:
        logger.debug(type(testcase))
        raise
    except BaseException:
        raise
    inp_file = click.open_file(inp_path, 'w')
    ans_file = click.open_file(ans_path, 'w')
    logger.debug('writing testcase %s for problem' % (testcase.code))
    inp_file.write(testcase.inp)
    ans_file.write(testcase.ans)
    inp_file.close()
    ans_file.close()


# judge_name is required for instantiating it back from file
def output_problem(problem, problem_dir):
    # TODO output
    # .problem(problem_data, problem_name, contest_name, judge_name)
    # output testcases
    try:
        assert isinstance(problem, Problem)
        directory_path = os.path.join(problem_dir, problem.code)
        problem_path = os.path.join(directory_path, '.problem.yml')
        logger.debug(problem_path)
        os.makedirs(directory_path)
    except FileExistsError:
        pass
    except AssertionError:
        logger.debug(type(problem))
        raise
    except BaseException:
        raise
    write(problem_path, None, problem)
    html_path = os.path.join(directory_path, problem.code + '.html')
    html_file = click.open_file(html_path, 'w')
    logger.debug('writing html for %s' % problem.code)
    html_file.write(problem.html)
    html_file.close()
    testcase_path = os.path.join(directory_path, 'testcases')
    for testcase in problem.testcases:
        output_testcase(testcase, testcase_path)


def output_contest(contest, contest_dir):
    # TODO output .contest(contest_data, contest_name, judge_name)
        # for each problem:
        #   output problem_data
        #   output testcases
    assert isinstance(contest, Contest)
    try:
        directory_path = os.path.join(contest_dir, contest.code)
        contest_path = os.path.join(directory_path, '.contest.yml')
        logger.debug(contest_path)
        os.makedirs(directory_path)
    except FileExistsError:
        pass
    except BaseException:
        raise
    write(contest_path, None, contest)
    logger.debug(contest.problems)
    for problem in contest.problems:
        output_problem(problem, directory_path)
