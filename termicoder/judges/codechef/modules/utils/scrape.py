"""
This module contatins function for scraping contest list, contest, problem
from codechef. The functions return dictionaries with errors and data
"""
import requests
import sys
import click
from bs4 import BeautifulSoup
import json
from time import strptime,strftime,mktime,gmtime,localtime
from termicoder.judges.codechef.modules.utils import session
from termicoder.utils import  display

def sanitize(io):
    """
    removes ":" "1:" etc if any in front of the io
    """
    # trim begining and ending spaces
    io = io.strip()
    # if Output: Input: etc.
    if(io[0]==":"):
        io=io[1:]
    # if Output1: Input1: etc
    elif(len(io)>1 and io[1]==":"):
        io=io[2:]
    return io.strip()+"\n"

def extract_io(pre_tag_elements,url):
    """
    extracts all input and output from pre tags and returns as tuple
    """
    sample_inputs=[]
    sample_outputs=[]
    for sample_io in pre_tag_elements:
        # finding heading / previous sibling of pre
        sibling = sample_io.previous_sibling
        while(not str(sibling).strip()):
            sibling = sibling.previous_sibling

        # converting sample_io to text
        iotext=str(sample_io.text)

        # standard codechef problems with input and output in same pre tag
        # OR sometimes input just above pre tag and output in pretag
        if( ("input" in iotext.lower() or "input" in str(sibling).lower() ) and "output" in iotext.lower()):
            in_index, out_index = iotext.lower().find("input"), iotext.lower().find("output")
            ki=1 if (in_index == -1) else 5
            sample_input = sanitize(iotext[in_index+ki : out_index])
            sample_output = sanitize(iotext[out_index + 6:])

            if(len(sample_inputs) != len(sample_outputs)):
                sample_inputs=[]
                sample_outputs=[]
            sample_inputs.append(sample_input)
            sample_outputs.append(sample_output)


        # problem with input only like challenge problems
        # or input and output in seperate pre tags
        elif("input" in str(sample_io.text).lower() or "input" in str(sibling).lower()):
            in_index = iotext.lower().find("input")
            ki=1 if (in_index == -1) else 5
            sample_input = sanitize(iotext[in_index+ki:])
            sample_inputs.append(sample_input)

        # problem with output only like printing 100! etc
        # or input and output in seperate pre tags
        elif("output" in str(sample_io.text).lower() or "output" in str(sibling).lower()):
            out_index = iotext.lower().find("output")
            ko=1 if (out_index == -1) else 6
            sample_output = sanitize(iotext[out_index+ko:])
            sample_outputs.append(sample_output)

    return sample_inputs,sample_outputs

def get_problem(problem_code,contest_code,abort):
    codechef_session = session.codechef_session
    # works on the fact that sample io will be inside pre tag and if more than 1 sample than more than 1 pre tag
    url="https://www.codechef.com/api/contests/"+contest_code+"/problems/"+problem_code
    j={"error":None,"judge":"codechef","contest_code":contest_code,"problem_code":problem_code}
    try:
        r = codechef_session.get(url)
        j.update(r.json())
    except:
        j["error"]="urlerror"
        click.echo('')
        display.url_error(url,abort=abort)
    else:
        if(j["status"]=="error"):
            click.echo('')
            click.echo("codechef returned following error:")
            display.error(j["message"])
            display.normal("There may be a problem with the problem code/contest code.\nPlease check and try again")
            if(abort):
                sys.exit()
        else:
            soup=BeautifulSoup(j['body'],"html.parser")

            pre_tag_elements=soup.find_all('pre')
            pre_tag_count=len(pre_tag_elements)
            sample_io={}
            if pre_tag_count >= 1:
                sample_inputs,sample_outputs = extract_io(pre_tag_elements,url)
                sample_io["inputs"]=sample_inputs
                sample_io["outputs"]=sample_outputs
                sample_io["error"]=None
            else:
                sample_io["error"]="Out of Scope"
                display.error("WARNING: the sample testcases of problem "+problem_code+
                " could not be extrated properly,\nplease have a look at the testcases folder")
            j["sample_io"]=sample_io
    return j

def get_contest(contest_code,abort):
    codechef_session = session.codechef_session
    url="https://www.codechef.com/api/contests/"+contest_code
    j={"error":None,"judge":"codechef","contest_code":contest_code}
    try:
        r = codechef_session.get(url)
        j.update(r.json())
    except:
        j["error"]="urlerror"
        click.echo("")
        display.url_error(url,abort=abort)
    if("error" in j["status"]):
        display.error("\n"+j["message"])
        if(abort==True):
            sys.exit()
    return j

def get_contest_list():
    codechef_session = session.codechef_session
    url="https://www.codechef.com/api/runningUpcomingContests/data"
    j={"error":None,"judge":"codechef","others":None}
    try:
        page = codechef_session.get(url)
        j.update(page.json())
    except:
        j["error"]="urlerror"
        display.url_error(url,abort=True)

    #try to add other contests (PRACTICE,ZCO etc)
    #(for which submissions are allowed)
    others=None
    try:
        url="https://www.codechef.com/api/allowed/contests"
        page = codechef_session.get(url)
        others=page.json()
        j["others"]=others
    except:
        pass

    return j


def get_practice_problems(category):
    categorylist=["school","easy","medium","hard","challenge","extcontest"]
    codechef_session = session.codechef_session
    url="https://www.codechef.com/problems"+category
    display.log("get practice problems not implemented in this version")
