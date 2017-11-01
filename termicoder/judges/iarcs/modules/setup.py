import click
import sys
import termicoder.utils.display as display
import termicoder.judges.iarcs.modules.utils.session as session
import termicoder.judges.iarcs.modules.utils.scrape as scrape
import os
import json


def login():
    click.echo("trying to get your login page...")
    if(session.is_logged_in(ensure=True)):
        display.normal("You are already logged in")
    else:
        username = click.prompt('enter username', type=click.STRING)
        password = click.prompt('enter password', type=click.STRING,
                                hide_input=True)
        display.normal("logging you into iarcs. please wait...")
        session.login(username, password)
        display.normal("you were logged in successfully. cookies saved")


def logout():
    if(not session.is_logged_in(ensure=False)):
        display.normal("invalid option --logout")
        display.normal("you are already logged out of iarcs")
    else:
        display.normal("logging you out of iarcs. please wait...")
        session.logout()
        display.normal("you were logged out sucessfully. cookies deleted")


def setup_problem(problem_code):
    problem_code = problem_code.upper()
    problem_path = os.path.join(".", problem_code)
    j = scrape.get_problem(problem_code)
    if(j["error"] is None):
        problem_html = j.pop("body")
        sample_io = j.pop("sample_io")

        try:
            os.mkdir(problem_path)
        except BaseException:
            pass

        problem_html_path = os.path.join(problem_path, problem_code+".html")
        phfile = open(problem_html_path, "w")
        click.echo(problem_html, file=phfile)

        if(not sample_io["error"]):
            testcases_path = os.path.join(problem_path, "testcases")
            try:
                os.mkdir(testcases_path)
            except BaseException:
                pass
            for i in range(len(sample_io["inputs"])):
                input_file = os.path.join(testcases_path, str(i+1)+".in")
                ifile = open(input_file, "w")
                click.echo(sample_io["inputs"][i], file=ifile, nl=False)
            for o in range(len(sample_io["outputs"])):
                output_file = os.path.join(testcases_path, str(o+1)+".out")
                ofile = open(output_file, "w")
                click.echo(sample_io["outputs"][o], file=ofile, nl=False)

        problem_file_path = os.path.join(problem_path, ".problem")
        problem_file = open(problem_file_path, "w")
        click.echo(json.dumps(j, indent=2), file=problem_file)


def setup_all_problems(confirm=True):
    if(confirm):
        click.confirm(
            "You have not passed any flag to iarcs.\n" +
            "Do you want to setup all problems?",
            default=True,
            abort=True)
    click.echo("trying to get your login status...", nl=False)
    status = session.is_logged_in(ensure=True)

    if(status):
        display.normal("\tDone\nYou are currently logged in, " +
                       "only unsolved problems will be setup")
    elif(status is False):
        display.normal("\tDone\nYou are currently logged out, " +
                       "all problems will be setup")
    else:
        display.error("Cannot determine login status\n" +
                      "Pls check your internet connection")
        sys.exit()

    cwd = os.getcwd()
    try:
        os.mkdir("iarcs")
    except BaseException:
        pass
    os.chdir("iarcs")
    click.echo("fetching problem list... ", nl=False)
    problem_list = scrape.get_problem_list()
    click.echo("\tDone")
    display.normal("setting up %d problems from iarcs..." % len(problem_list))
    with click.progressbar(problem_list) as bar:
        for problem in bar:
            setup_problem(problem["problem_code"])
    os.chdir(cwd)
