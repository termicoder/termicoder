import click
import termicoder.utils.display as display
import termicoder.judges.iarcs.modules.utils.session as session

def login():
    if(session.is_logged_in()==True):
        display.normal("You are already logged in")
    else:
        display.normal("logging you into iarcs. please wait...")
        session.login()

def logout():
    display.normal("logging you out of iarcs. please wait...")
    session.logout()


def problem(problem_code):
    display.normal("setup problem not implemented yet")
