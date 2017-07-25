"""
this module creates the required files of a contest/problem including
json data of contest(.contest file), json data of problem(.problem file)
html problem statements and testcases
"""
import click
import termicoder.utils.display as display
import termicoder.judges.codechef.modules.utils.session as session
import termicoder.judges.codechef.modules.utils.scrape as scrape
import os
import json
normal_problem_types=["3","0"]

def login():
    click.echo("trying to get your login page...")
    if(session.is_logged_in(ensure=True)==True):
        display.normal("You are already logged in")
    else:
        username=click.prompt('enter username', type=click.STRING)
        password=click.prompt('enter password', type=click.STRING,
                                hide_input=True)
        display.normal("logging you into codechef. please wait...")
        session.login(username,password)
        display.normal("you were logged in successfully. cookies saved")

def logout():
    if(session.is_logged_in(ensure=False) == False):
        display.normal("invalid option --logout")
        display.normal("you are already logged out of iarcs")
    else:
        display.normal("logging you out of codechef. please wait...")
        session.logout()
        display.normal("you were logged out sucessfully. cookies deleted")

def setup_problem(problem_code,contest_code,abort):
    problem_code=problem_code.upper()
    contest_code=contest_code.upper()
    problem_path=os.path.join(".",problem_code)

    try:
        os.mkdir(problem_path)
    except:
        pass
    problem=scrape.get_problem(problem_code,contest_code,abort=abort)
    if problem["error"]==None:
        problem_html=problem.pop("body")
        sample_io=problem.pop("sample_io")
        # html problem statement
        if not problem["error"]:
            problem_html_path=os.path.join(problem_path,problem_code+".html")
            phfile=open(problem_html_path,"w")
            click.echo(problem_html,file=phfile)

        # sample_io files
        if(sample_io["error"]==None):
            testcases_path=os.path.join(problem_path,"testcases")
            try:
                os.mkdir(testcases_path)
            except:
                pass
            for i in range(len(sample_io["inputs"])):
                input_file=os.path.join(testcases_path,str(i+1)+".in")
                ifile=open(input_file,"w")
                click.echo(sample_io["inputs"][i],file=ifile,nl=False)
            for o in range(len(sample_io["outputs"])):
                output_file=os.path.join(testcases_path,str(o+1)+".out")
                ofile=open(output_file,"w")
                click.echo(sample_io["outputs"][o],file=ofile,nl=False)

    # the problem data
    problem_setup_file=os.path.join(problem_path,".problem")
    f1=open(problem_setup_file,"w")
    click.echo(json.dumps(problem,indent=2,sort_keys=True),file=f1)


def setup_contest(contest_code,abort):
    contest_code=contest_code.upper()
    contest_path=os.path.join(".",contest_code)
    click.echo("requesting data for contest %s. Please wait..."%contest_code,nl=False)
    contest_data=scrape.get_contest(contest_code,abort=abort)

    if(contest_data["error"] is None):
        click.echo("\t Done")

    if(contest_data["user"]["username"] is not None):
        click.echo("you are currently logged in."+
        "\ncompletely solved problems will not be setup"+
        "\nthough if you want you can set them up individually later")
    else:
        click.echo("you are currently NOT logged in."+
        "\nALL problems of the contest will be setup")

    problems_to_setup=[]
    for i in contest_data["problems"]:
        if(i not in contest_data["problemsstats"]["solved"] or
        contest_data["problems"][i]["type"] not in normal_problem_types or
        i in contest_data["problemsstats"]["partially_solved"]):
            problems_to_setup.append(contest_data["problems"][i])

    try:
        os.mkdir(contest_path)
    except:
        pass

    contest_setup_file=os.path.join(contest_path,".contest")
    f=open(contest_setup_file,"w")
    if(contest_data["error"]==None):
        del contest_data["rules"]
    click.echo(json.dumps(contest_data,indent=2), file=f)

    # setup all problems for the contests
    problem_list=[problem["code"] for problem in problems_to_setup]
    directory=os.getcwd()
    os.chdir(contest_path)
    if(contest_data["error"]==None):
        with click.progressbar(problem_list) as bar:
            for problem_code in bar:
                setup_problem(problem_code,contest_code,abort=False)
    os.chdir(directory)

def setup_practice():
    click.echo("setup PRACTICE not implemted in this version")
    return None
