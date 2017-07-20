"""
This module contatins function for scraping contest list, contest, problem
from codechef. The function return dictionaries with errors and data
"""
import requests
import sys
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

def get_problem(problem_code,contest_code="PRACTICE"):
    codechef_session = session.codechef_session
    # works on the fact that sample io will be inside pre tag and if more than 1 sample than more than 1 pre tag
    url="https://www.codechef.com/api/contests/"+contest_code+"/problems/"+problem_code
    j={"error":None,"judge":"codechef","contest_code":contest_code,"problem_code":problem_code}
    try:
        r = codechef_session.get(url)
        j.update(r.json())
        soup=BeautifulSoup(j['body'],"html.parser")
    except:
        j["error"]="urlerror"
    else:
        pre_tag_elements=soup.find_all('pre')
        pre_tag_count=len(pre_tag_elements)
        sample_io={}
        if pre_tag_count >= 1:
            sample_inputs,sample_outputs = extract_io(pre_tag_elements,url)
            sample_io["inputs"]=sample_inputs
            sample_io["outputs"]=sample_outputs
            sample_io["error"]=""
        else:
            sample_io["error"]="Out of Scope"
        j["sample_io"]=sample_io
        j["judge"]="codechef"
    return j

def get_contest(contest_code,abort=True):
    codechef_session = session.codechef_session
    url="https://www.codechef.com/api/contests/"+contest_code
    j={"error":None,"judge":"codechef","contest_code":contest_code}
    try:
        r = codechef_session.get(url)
        j.update(r.json())
    except:
        j["error"]="urlerror"
        display.url_error(url,abort=abort)
    if("error" in j["status"]):
        display.error(j["message"])
        if(abort==True):
            sys.exit()
    return j


# The following function is derived from CoderCalender
# https://github.com/nishanthvijayan/CoderCalendar
# published under GNU GPL 3.0

def get_duration(duration):
    days = duration/(60*24)
    duration %= 60*24
    hours = duration/60
    duration %= 60
    minutes = duration
    ans=""
    if days==1: ans += str(days)+" day "
    elif days!=0: ans +=str(days)+" days "
    if hours!=0: ans += str(hours)+"h "
    if minutes!=0: ans += str(minutes)+"m"
    return ans.strip()

# The following function is derived from CoderCalender
# https://github.com/nishanthvijayan/CoderCalendar
# published under GNU GPL 3.0
# functionality for past contests is added.
# now using problem code instead of url

def  get_contest_list():
    codechef_session = session.codechef_session
    url="http://www.codechef.com/contests"
    contests= {"ongoing":[] , "upcoming":[], "past":[],"error":None}
    try:
        page = codechef_session.get(url)
    except:
        contests["error"]="urlerror"
    else:
        soup = BeautifulSoup(page.text, "html.parser")

        contest_tables = {"Future Contests": [], "Present Contests": [],"Past Contests":[]}
        # links contest table to posts
        links = {"Future Contests": "upcoming", "Present Contests": "ongoing" ,"Past Contests":"past"}

        statusdiv = soup.findAll("table", attrs = {"class": "dataTable"})
        headings = soup.findAll("h3")

        for i in range(len(headings)):
            contest_tables[headings[i].text] = statusdiv[i].findAll("tr")[1:]

        for tense in links:
            for some_contest in contest_tables[tense]:
                details = some_contest.findAll("td")
                start_time = strptime(details[2].text, "%d %b %Y %H:%M:%S")
                end_time = strptime(details[3].text, "%d %b %Y %H:%M:%S")
                duration = get_duration(int((mktime(end_time) - mktime(start_time)) / 60))
                contests[links[tense]].append({"Name":  details[1].text,
                                          "code":  details[1].a["href"][1:],
                                          "StartTime": strftime("%a, %d %b %Y %H:%M", start_time),
                                          "EndTime": strftime("%a, %d %b %Y %H:%M", end_time),
                                          "Duration": duration,
                                          "Platform": "codefhef"})
    return contests

def get_running_contests():
    codechef_session = session.codechef_session
    url="https://www.codechef.com/api/runningUpcomingContests/data"
    j={"error":None,"judge":"codechef"}
    try:
        page = codechef_session.get(url)
        j.update(page.json())
    except:
        j["error"]="urlerror"
    return j


def get_practice_problems(category):
    categorylist=["school","easy","medium","hard","challenge","extcontest"]
    codechef_session = session.codechef_session
    url="https://www.codechef.com/problems"+category
    display.log("Not implemented yet")
