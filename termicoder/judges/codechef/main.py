'''
this file first handles error/input with respect to this
judge and then forwards the request to correct module/function
'''

import click
import termicoder.utils.display as display
import termicoder.judges.codechef.modules.view as view_module
import termicoder.judges.codechef.modules.setup as setup_module
import termicoder.judges.codechef.modules.submit as submit_module
import termicoder.judges.codechef.modules.utils.session as session

# try to load old session(if exists) before doing anything
session.load()


def view_contests():
    view_module.contests()


def view_problems(contest_code):
    # if empty contest code, get one here
    if(not contest_code):
        contest_code = click.prompt("please enter a contest code",
                                    type=click.STRING, default="PRACTICE")

    if(contest_code):
        view_module.problems(contest_code)
    else:
        # TODO remove this later
        display.error("some error with contest code... It shouldn't be empty")


def setup(contest_code, problem_code, status):
    if(status == "login"):
        setup_module.login()
    elif(status == "logout"):
        setup_module.logout()

    if(contest_code is None and status is None):
        contest_code = click.prompt("please enter a contest code",
                                    type=click.STRING, default="PRACTICE")

    if(contest_code is not None):
        if(problem_code is not None):
            click.echo(
                "requesting problem %s from contest %s. please wait..." %
                (problem_code.upper(), contest_code.upper()), nl=False)
            setup_module.setup_problem(problem_code, contest_code, abort=True)
            click.echo("\t Done")
        elif(problem_code is None):
            setup_module.setup_contest(contest_code, abort=True)


def submit(code_file):
    submit_module.submit(code_file)
