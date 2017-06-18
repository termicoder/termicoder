#import click
import requests
from bs4 import BeautifulSoup
import json
from time import strptime,strftime,mktime,gmtime,localtime
import sys
sys.stdout = open('logs.txt', 'w')

def get_duration(duration):
    days = duration/(60*24)
    duration %= 60*24
    hours = duration/60
    duration %= 60
    minutes = duration
    ans=""
    if days==1: ans+=str(days)+" day "
    elif days!=0: ans+=str(days)+" days "
    if hours!=0:ans+=str(hours)+"h "
    if minutes!=0:ans+=str(minutes)+"m"
    return ans.strip()

def get_problem(contest_code,problem_code):
    #works on the fact that sample io will be inside pre tag and if more than 1 sample than more than 1 pre tag
    url="https://www.codechef.com/api/contests/"+contest_code+"/problems/"+problem_code
    try:
        r = requests.get(url)
        j= json.loads(r.text)
        soup=BeautifulSoup(j['body'],"html.parser")
    except:
         print("error in fetching url:\n" + url)
    else:
        #loop because there can be others pre in a problem example https://www.codechef.com/JUNE17/problems/PRMQ or multiple pre for multiple test cases
        for sampleio in soup.find_all('pre'):
            try:
                sample_input=str(sampleio.b.next_sibling).strip()+"\n"
                sample_output=str(sampleio.b.next_sibling.next_sibling.next_sibling).strip()+"\n"

                #fix for problems like https://www.codechef.com/JUNE17/problems/XENRANK
                if(sample_input[0] is ":"):
                    sample_input=sample_input[1:].strip()+"\n"
                if(sample_output[0] is ":"):
                    sample_output=sample_output[1:].strip()+"\n"
                print("input\n"+sample_input)
                print("output\n"+sample_output)
                #endfix
            except:
                #TODO create a log of the exception
                print("error get testcase")
                continue
    sys.stdout.flush()

'''
exceptions to above
https://www.codechef.com/IOIPRAC/problems/INOI1201
'''

def get_contest(contest_code):
    url="https://www.codechef.com/api/contests/"+contest_code
    try:
        r = requests.get(url)
        j= json.loads(r.text)
    except:
        print("error in fetching url:\n" + url)
    else:
        problems=j["problems"]
        for problem in problems:
            print(contest_code,problems[problem]["code"],problems[problem]["name"],str(problems[problem]["successful_submissions"]))
            try:
                get_problem(contest_code,problems[problem]["code"])
            except:
                print("error geting problem",problems[problem]["code"])


#The following function is derived from codercalender
#TODO include links of licence and author etc.
#functionality for past contests is added.
#now using problem code instead of url


def  get_contest_list():
    url="http://www.codechef.com/contests"
    page = requests.get(url)
    print("got the list")
    soup = BeautifulSoup(page.text, "html.parser")

    posts= {"ongoing":[] , "upcoming":[], "past":[]}
    statusdiv = soup.findAll("table", attrs = {"class": "dataTable"})
    headings = soup.findAll("h3")
    contest_tables = {"Future Contests": [], "Present Contests": [],"Past Contests":[]}
    for i in range(len(headings)):
        contest_tables[headings[i].text] = statusdiv[i].findAll("tr")[1:]

    for upcoming_contest in contest_tables["Future Contests"]:
        details = upcoming_contest.findAll("td")
        start_time = strptime(details[2].text, "%d %b %Y %H:%M:%S")
        end_time = strptime(details[3].text, "%d %b %Y %H:%M:%S")
        duration = get_duration(int((mktime(end_time) - mktime(start_time)) / 60))
        posts["upcoming"].append({"Name":  details[1].text,
                                  "code":  details[1].a["href"][1:],
                                  "StartTime": strftime("%a, %d %b %Y %H:%M", start_time),
                                  "EndTime": strftime("%a, %d %b %Y %H:%M", end_time),
                                  "Duration": duration,
                                  "Platform": "CODECHEF"})
        print("contest "+details[1].a["href"][1:])
        #get_contest(str(details[1].a["href"][1:]))

    for present_contest in contest_tables["Present Contests"]:
        details = present_contest.findAll("td")
        start_time = strptime(details[2].text, "%d %b %Y %H:%M:%S")
        end_time = strptime(details[3].text, "%d %b %Y %H:%M:%S")
        posts["ongoing"].append({"Name":  details[1].text,
                                 "code":  details[1].a["href"][1:],
                                 "StartTime": strftime("%a, %d %b %Y %H:%M", start_time),
                                 "EndTime": strftime("%a, %d %b %Y %H:%M", end_time),
                                 "Platform": "CODECHEF"})
        print("contest "+details[1].a["href"][1:])
        try:
            get_contest(str(details[1].a["href"][1:]))
        except:
            print("error get contest",str(details[1].a["href"][1:]))

    for past_contest in contest_tables["Past Contests"]:
        details = past_contest.findAll("td")
        start_time = strptime(details[2].text, "%d %b %Y %H:%M:%S")
        end_time = strptime(details[3].text, "%d %b %Y %H:%M:%S")
        posts["past"].append({"Name":  details[1].text,
                                 "code":  details[1].a["href"][1:],
                                 "StartTime": strftime("%a, %d %b %Y %H:%M", start_time),
                                 "EndTime": strftime("%a, %d %b %Y %H:%M", end_time),
                                 "Platform": "CODECHEF"})
        print("contest "+details[1].a["href"][1:])
        try:
            get_contest(str(details[1].a["href"][1:]))
        except:
             print("error get contest",str(details[1].a["href"][1:]))

        #print(posts["past"])

get_contest_list()
