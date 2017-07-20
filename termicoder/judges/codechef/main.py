'''
this file first handles error/input with respet to this
judge and then forwards the request to correct module/function
'''

import click
import sys
import termicoder.utils.display as display
import termicoder.judges.codechef.modules.view as view_module
import termicoder.judges.codechef.modules.setup as setup_module
import termicoder.judges.codechef.modules.submit as submit_module
import termicoder.judges.codechef.modules.utils.session as session

# try to load old session(if exists) before doing anything
session.load()

def view_contests():
    view_module.contests()

def view_problems(contest):
    if(contest is None):
        contest=click.prompt("Please enter a contest code",default="PRACTICE")
    view_module.problems(contest)

def setup(contest, problem, status):
    if(status=="login"):
        setup_module.login()
    elif(status=="logout"):
        setup_module.logout()


    # if(problem_code is not None):
    #     click.echo("setting up problem "+problem_code.upper()+
    #     " from codechef...",nl=False)
    #     setup_module.setup_problem(problem_code)
    #     click.echo("\tDone")

    #elif(status is None  and problem_code is None):
    #    setup_module.setup_all_problems(confirm=True)
