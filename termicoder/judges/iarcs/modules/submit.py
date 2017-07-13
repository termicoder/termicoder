# FIXME: poor error checking for this module
import os
import json
import click
import requests
from bs4 import BeautifulSoup
import time
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
    soup=BeautifulSoup(html,"html.parser")
    code_body=str(soup.find(id="maincontent").get_text(strip=True))
    code=(code_body.split(' ')[2])
    return(code)

def check_status(code):
    delay=1
    iarcs_session=session.iarcs_session
    url="http://opc.iarcs.org.in/index.php/results/"+str(code)

    status="compiling"
    while("running" in status.lower() or "compiling" in status.lower()):
        r=iarcs_session.get(url)
        soup=BeautifulSoup(r.text,"html.parser")
        body=soup.find(id="maincontent")
        status=body.findAll("p")[1].text.split(' ',1) [1]
        time.sleep(delay)
    points=body.findAll("p")[2].text.rsplit(' ',1)[1]
    return status, points

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
    click.echo("retriving status (you can continue your work in another tab)...",
                nl=False)

    submission_code=get_submission_code(r.text)
    status,points=check_status(submission_code)
    click.echo("\tDone")
    click.echo("status: "+status)
    click.echo("points: "+points)
