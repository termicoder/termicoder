"""
This module contatins function for scraping contest list, contest, problem
from codechef. The functions return dictionaries with errors and data
"""

import sys
import click
from bs4 import BeautifulSoup
from termicoder.judges.codechef.modules.utils import session
from termicoder.utils import display


def sanitize(io):
    """
    removes ":" "1:" etc if any in front of the io
    """
    # trim begining and ending spaces
    io = io.strip()
    # if Output: Input: etc.
    if(io[0] == ":"):
        io = io[1:]
    # if Output1: Input1: etc
    elif(len(io) > 1 and io[1] == ":"):
        io = io[2:]
    return io.strip()+"\n"


def extract_io(pre_tag_elements, url):
    """
    extracts all input and output from pre tags and returns as tuple
    """
    sample_inputs = []
    sample_outputs = []
    for sample_io in pre_tag_elements:
        # finding heading / previous sibling of pre
        sibling = sample_io.previous_sibling
        while(not str(sibling).strip()):
            sibling = sibling.previous_sibling

        # converting sample_io to text
        iotext = str(sample_io.text)

        # standard codechef problems with input and output in same pre tag
        # OR sometimes input just above pre tag and output in pretag
        if(("input" in iotext.lower() or "input" in str(sibling).lower()) and
           "output" in iotext.lower()):
            in_index, out_index = iotext.lower().find(
                "input"), iotext.lower().find("output")
            ki = 1 if (in_index == -1) else 5
            sample_input = sanitize(iotext[in_index+ki: out_index])
            sample_output = sanitize(iotext[out_index + 6:])

            if(len(sample_inputs) != len(sample_outputs)):
                sample_inputs = []
                sample_outputs = []
            sample_inputs.append(sample_input)
            sample_outputs.append(sample_output)

        # problem with input only like challenge problems
        # or input and output in seperate pre tags
        elif("input" in str(sample_io.text).lower() or
             "input" in str(sibling).lower()):
            in_index = iotext.lower().find("input")
            ki = 1 if (in_index == -1) else 5
            sample_input = sanitize(iotext[in_index+ki:])
            sample_inputs.append(sample_input)

        # problem with output only like printing 100! etc
        # or input and output in seperate pre tags
        elif("output" in str(sample_io.text).lower() or
             "output" in str(sibling).lower()):
            out_index = iotext.lower().find("output")
            ko = 1 if (out_index == -1) else 6
            sample_output = sanitize(iotext[out_index+ko:])
            sample_outputs.append(sample_output)

    return sample_inputs, sample_outputs


def get_problem(problem_code, contest_code, abort):
    codechef_session = session.codechef_session
    # works on the fact that sample io will be inside pre tag and if more than
    # 1 sample than more than 1 pre tag
    url = "https://www.codechef.com/api/contests/" + contest_code +\
        "/problems/" + problem_code

    j = {
        "error": None,
        "judge": "codechef",
        "contest_code": contest_code,
        "problem_code": problem_code}
    try:
        r = codechef_session.get(url)
        j.update(r.json())
    except BaseException:
        j["error"] = "urlerror"
        click.echo('')
        display.url_error(url, abort=abort)
    else:
        if(j["status"] == "error"):
            click.echo('')
            click.echo("codechef returned following error:")
            display.error(j["message"])
            display.normal(
                "There may be a problem with the problem code/contest code." +
                "\nPlease check and try again")
            if(abort):
                sys.exit()
        else:
            soup = BeautifulSoup(j['body'], "html.parser")

            pre_tag_elements = soup.find_all('pre')
            pre_tag_count = len(pre_tag_elements)
            sample_io = {}
            if pre_tag_count >= 1:
                sample_inputs, sample_outputs = extract_io(
                    pre_tag_elements, url)
                sample_io["inputs"] = sample_inputs
                sample_io["outputs"] = sample_outputs
                sample_io["error"] = None
            else:
                sample_io["error"] = "Out of Scope"
                display.error(
                    "WARNING:the sample testcases of problem " + problem_code +
                    " could not be extrated properly,\n" +
                    "please have a look at the testcases folder")
            j["sample_io"] = sample_io
    return j


def get_contest(contest_code, abort):
    codechef_session = session.codechef_session
    url = "https://www.codechef.com/api/contests/"+contest_code
    j = {"error": None, "judge": "codechef", "contest_code": contest_code}
    try:
        r = codechef_session.get(url)
        j.update(r.json())
    except BaseException:
        j["error"] = "urlerror"
        click.echo("")
        display.url_error(url, abort=abort)
    if("error" in j["status"]):
        display.error("\n"+j["message"])
        if(abort):
            raise click.Abort
    return j


def get_contest_list():
    codechef_session = session.codechef_session
    url = "https://www.codechef.com/api/runningUpcomingContests/data"
    j = {"error": None, "judge": "codechef", "others": None}
    try:
        page = codechef_session.get(url)
        j.update(page.json())
    except BaseException:
        j["error"] = "urlerror"
        display.url_error(url, abort=True)

    # try to add other contests (PRACTICE,ZCO etc)
    # (for which submissions are allowed)
    others = None
    try:
        url = "https://www.codechef.com/api/allowed/contests"
        page = codechef_session.get(url)
        others = page.json()
        j["others"] = others
    except BaseException:
        pass

    return j


def get_practice_problems(catagory, abort):
    catagory = str(catagory)
    codechef_session = session.codechef_session
    url = "https://www.codechef.com/problems/"+catagory
    j = {"error": None, "judge": "codechef", "contest_code": "PRACTICE"}
    data = {
        "sort_by": "SucessfulSubmission",
        "sorting_order": "desc"
    }
    try:
        practice_page = codechef_session.get(url, data=data)
    except BaseException:
        j["error"] = "urlerror"
        click.echo("")
        display.url_error(url, abort=abort)
    else:
        soup = BeautifulSoup(practice_page.text, 'html.parser')
        problem_rows = soup.find_all('tr', class_='problemrow')
        problems = {}
        problemsstats = {
                'attempted': {},
                'partially_solved': {},
                'solved': {}
            }
        for problem_row in problem_rows:
            problem_data = problem_row.find_all('td')
            # TODO partially implimented dictionary... may lead to error
            problem = {
                'code': problem_data[1].get_text(strip=True),
                'name': problem_data[0].get_text(strip=True),
                'type': "1" if catagory.lower() == "challenge" else "3",
                'successful_submissions': problem_data[2].get_text(strip=True),
                'allow_submissions': True,
                'accuracy': problem_data[3].get_text(strip=True),
            }
            problems[problem['code']] = problem
            try:
                if('green' in problem_data[0].a['style']):  # solved
                    problemsstats['attempted'][problem['code']] = True
                    problemsstats['solved'][problem['code']] = True
                elif('red' in problem_data[0].a['style']):  # wrong
                    problemsstats['attempted'][problem['code']] = True
                else:
                    # TODO partially solved problem...to be handled later
                    # TODO assinging 30 for convienence change later
                    problemsstats['attempted'][problem['code']] = True
                    problemsstats['partially_solved'][problem['code']] = 30
            except BaseException:
                # unsolved problems
                pass

        # the dictionary to be returned..similar to one returned by codechef
        # TODO partially implimented dictionary... may lead to error

        # find username next
        tempindex = practice_page.text.find("username")
        ustart = practice_page.text.find(":", tempindex)
        uend = practice_page.text.find("}", ustart)
        username = practice_page.text[ustart+1:uend]
        if(username == "null"):
            username = None
        else:
            username = username[1:-1]

        j.update({
            'status': 'success',
            'user': {
                'username': username
            },
            'code': "PRACTICE",
            'name': "PRACTICE/"+catagory.upper(),
            'problems': problems,
            'problemsstats': problemsstats,
            'rank_and_score': None,
            'practice_catagory': catagory,
            'rules': None
        })
    return j
