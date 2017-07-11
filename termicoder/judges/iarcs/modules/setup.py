import click
import termicoder.utils.display as display
import termicoder.judges.iarcs.modules.utils.session as session
import termicoder.judges.iarcs.modules.utils.scrape as scrape
import os
import json

def login():
    if(session.is_logged_in(ensure=True)==True):
        display.normal("You are already logged in")
    else:
        username=click.prompt('enter username', type=click.STRING)
        password=click.prompt('enter password', type=click.STRING,
                                hide_input=True)
        display.normal("logging you into iarcs. please wait...")
        session.login(username,password)
        display.normal("you were logged in successfully. cookies saved")


def logout():
    if(session.is_logged_in(ensure=False) == False):
        display.normal("invalid option --logout")
        display.normal("you are already logged out of iarcs")
    else:
        display.normal("logging you out of iarcs. please wait...")
        session.logout()
        display.normal("you were logged out sucessfully. cookies deleted")


def setup_problem(problem_code):
    problem_path=os.path.join(".",problem_code)
    problem_code=problem_code.upper()
    click.echo("working on problem %s from iarcs. pls wait..." % problem_code)
    j=scrape.get_problem(problem_code)
    if(j["error"]==None):
        problem_html=j.pop("body")
        sample_io=j.pop("sample_io")

        try:
            os.mkdir(problem_path)
        except:
            pass

        problem_html_path=os.path.join(problem_path,problem_code+".html")
        phfile=open(problem_html_path,"w")
        click.echo(problem_html,file=phfile)

        if(not sample_io["error"]):
            testcases_path=os.path.join(problem_path,"testcases")
            try:
                os.mkdir(testcases_path)
            except:
                pass
            for i in range(len(sample_io["inputs"])):
                input_file=os.path.join(testcases_path,str(i+1)+".in")
                ifile=open(input_file,"w")
                print(sample_io["inputs"][i],file=ifile)
            for o in range(len(sample_io["outputs"])):
                output_file=os.path.join(testcases_path,str(o+1)+".out")
                ofile=open(output_file,"w")
                print(sample_io["outputs"][o],file=ofile)

        problem_file_path=os.path.join(problem_path,".problem")
        problem_file=open(problem_file_path,"w")
        click.echo(json.dumps(j,indent=2),file=problem_file)

        display.normal("data for problem %s is now setup"%problem_code)

def setup_all_problems():
    cwd=os.getcwd()
    display.normal("setting up all problems from iarcs. pls wait...")
    try:
        os.mkdir("iarcs")
        os.chdir("iarcs")
    except:
        pass
    problem_list=scrape.get_problem_list()
    for problem in problem_list:
        setup_problem(problem["problem_code"])
    os.chdir(cwd)
