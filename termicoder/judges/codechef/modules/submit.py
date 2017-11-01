# FIXME: poor error checking for this module
import os
import sys
import termicoder.judges.codechef.modules.utils.session as session
import termicoder.judges.codechef.modules.setup as setup_module
import termicoder.utils.display as display
import time
import json
import click

lang_map = {
    ".py": "python",
    ".java": "java",
    ".c": "c",
    ".cpp": "c++14",
    ".cc": "c++14",
    ".c++": "c++14"
}

lang_code_map = {
    "c++14": 44,
    "c": 11,
    "python2": 4,
    "python3": 116,
    "java": 10
}


def check_status(upid):
    delay = 2
    codechef_session = session.codechef_session
    check_url = "https://www.codechef.com/api/ide/submit"
    payload = {"solution_id": upid}
    r = codechef_session.get(check_url, params=payload)
    try:
        status = r.json()
    except BaseException:
        status = None

    # maxtries such that max 3 minutes
    maxtries = 180//delay+1
    i = 0
    while(status is not None and
          status["result_code"] == 'wait' and
          i < maxtries):
        i += 1
        time.sleep(delay)
        r = codechef_session.get(check_url, params=payload)
        try:
            status = r.json()
        except BaseException:
            status = None
    # if still the first 2 conditions hold
    if(status is not None and status["result_code"] == 'wait'):
        display.error("\nMax tries("+str(maxtries)+")exceeded\n" +
                      "seems that judge is too busy\n" +
                      "the last status returned by judge was:")
        click.echo("status: "+json.dumps(status, indent=2))
        sys.exit()
    else:
        return status


def submit(code_file, submit_to_practice=False):
    # TODO check if it is able to submit(allowed)
    codechef_session = session.codechef_session
    submit_url = "https://www.codechef.com/api/ide/submit"

    problem_file = open(".problem")
    j = json.load(problem_file)
    problem_code = j["problem_code"]
    contest_code = j["contest_code"]

    if(submit_to_practice):
        contest_code = "PRACTICE"

    extension = os.path.splitext(code_file)[1]

    try:
        solution_text = open(code_file, 'r').read()
    except BaseException:
        display.error("The code file could not be loaded")
        sys.exit()

    try:
        lang = lang_map[extension]
        if(lang == "python"):
            ver = click.prompt(
                "Enter python version", type=click.Choice(["2", "3"]),
                default="3")
            lang = lang+ver
        lang_code = lang_code_map[lang]
    except BaseException:
        click.echo("the following extension is not supported:"
                   + extension)
        sys.exit()

    submit_data = {
        "sourceCode": solution_text,
        "problemCode": problem_code,
        "contestCode": contest_code,
        "language": lang_code
    }

    # final confirmation
    click.confirm("following problem will be submitted\n" +
                  "judge: codechef\n" +
                  "problem code: "+problem_code+"\n" +
                  "contest code: "+contest_code+"\n" +
                  "file: "+str(code_file)+"\n" +
                  "lang: "+lang+"\n"
                  "Are you sure?", default=True, abort=True)

    display.normal("checking your login...")
    login_status = session.is_logged_in(ensure=True)
    if(login_status is False):
        display.normal("You are NOT logged in. Redirecting to login...")
        setup_module.login()
    elif(login_status):
        display.normal("You are logged in")
    else:
        display.error("cannot determine login status\n" +
                      "please check your internet connection")
        sys.exit()

    click.echo("submitting your solution...", nl=False)

    try:
        a = codechef_session.post(submit_url, data=submit_data)
        j = a.json()
        assert(a.status_code == 200)
    except BaseException:
        display.url_error(submit_url, abort=True)

    if(j['status'] == "error"):
        display.normal("\nCodechef returned following errors:")
        display.error("\n".join(j['errors']))
        click.confirm(
            "Do you want to try to submitting to practice section instead?",
            default=True)
        submit(code_file, submit_to_practice=True)
    else:
        display.normal("\tDone")
        click.echo(
            "retriving status (you can continue your work in another tab)...",
            nl=False)
        status = check_status(j["upid"])
        click.echo("\tDone")
        click.echo("status: "+json.dumps(status, indent=2))
