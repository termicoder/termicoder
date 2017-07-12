# FIXME: poor error checking for this module
import os
import json
import click
import requests
import termicoder.judges.iarcs.modules.setup as setup_module
import termicoder.judges.iarcs.modules.utils.session as session
import termicoder.utils.display as display

lang_map={
".py":"python",
".java":"gcj",
".c":"c",
".cpp":"cpp",
".cc":"cpp",
".c++":"cpp"
}
def get_submission_code(html):
    print("get_submission_code not implemented yet")

def check_status(code):
    print("check_status not implemented yet")

    
def submit(code_file):
    iarcs_session=session.iarcs_session
    problem_file=open(".problem")
    j=json.load(problem_file)
    submit_url="http://opc.iarcs.org.in/index.php/submit/upload"

    probid=j["problem_code"]
    source=open(code_file,"rb")
    lang=lang_map[os.path.splitext(code_file)[1]]

    files={
    "source":source
    }

    data={
    "MAX_FILE_SIZE":"100000",
    "probid":probid,
    "lang":lang
    }

    # final confirmation
    click.confirm("following problem will be submitted\n"+
    "judge: iarcs\n"+
    "problem code: "+probid+"\n"+
    "file: "+str(code_file)+"\n"+
    "lang: "+lang+"\n"
    "Are you sure?",default=True,abort=True)

    display.normal("checking your login...")
    if(session.is_logged_in(ensure=True)==False):
        display.normal("You are not already logged in. Redirecting to login...")
        setup_module.login()
    else:
        display.normal("You are logged in")
    #confirm submit
    click.echo("submitting your solution...",nl=False)
    # TODO: test before submit
    r=iarcs_session.post(submit_url,files=files,data=data)
    display.normal("\tDone")
    display.normal("retriving status (you can continue your work in another tab)...")

    submission_code=get_submission_code(r.text)
    a=check_status(submission_code)
