'''
this file first handles error/input with respet to this
judge and then forwards the request to correct module/function
'''

import click
import termicoder.utils.display as display
import termicoder.judges.iarcs.modules.view as view_module
import termicoder.judges.iarcs.modules.setup as setup_module
import termicoder.judges.iarcs.modules.submit as submit_module
import termicoder.judges.iarcs.modules.utils.session as session


# try to load old session(if exists) before doing anything
session.load()


def view_contests():
    display.error("iarcs does not hold any contests")
    display.normal("you can view problems through:")
    display.command("termicoder view problems -j iarcs")


def view_problems(contest):
    try:
        assert(contest is None)
    except BaseException:
        display.error("unexpected input --contest for judge iarcs")
        display.normal("try:")
        display.command("termicoder view problems -j iarcs")
    else:
        view_module.problems()


def setup(contest, problem_code, status):
    try:
        assert(contest is None)
    except BaseException:
        display.error("unexpected input --contest for judge iarcs")
        display.normal("try:")
        display.command("termicoder view problems -j iarcs")
    else:
        if(status == "login"):
            setup_module.login()
        elif(status == "logout"):
            setup_module.logout()

        if(problem_code is not None):
            click.echo("setting up problem "+problem_code.upper() +
                       " from iarcs...", nl=False)
            setup_module.setup_problem(problem_code)
            click.echo("\tDone")

        elif(status is None and problem_code is None):
            setup_module.setup_all_problems(confirm=True)


def submit(code_file):
    submit_module.submit(code_file)
