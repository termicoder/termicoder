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
    click.echo("setup not implemented yet")
