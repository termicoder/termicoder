from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import json
from time import strptime,strftime,mktime,gmtime,localtime
import sys
sys.stdout = open('./logs/logs.txt', 'w')
sys.stderr = open('./logs/errors.txt', 'w')
urlerr = open("./logs/url_error.txt",'w')
count = open("./logs/count.txt",'w')
out_of_scope = open("./logs/out_of_scope.txt",'w')
problem_count=0
error_count=0
correct_count=0


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()

def urlerror(*args, **kwargs):
    print(*args, file=urlerr, **kwargs)
    urlerr.flush()

def count_print(*args, **kwargs):
    print(*args, file=count, **kwargs)
    count.flush()

def scope_err_print(*args, **kwargs):
    print(*args, file=out_of_scope, **kwargs)
    out_of_scope.flush()

def extract_io(pre_tag_elements,url):
    sample_inputs=[]
    sample_outputs=[]
    for sampleio in pre_tag_elements:
        sibling=sampleio.previous_sibling
        while(not str(sibling).strip()):
            sibling=sibling.previous_sibling     
        #standard codechef problems with input and output in same pre tag
        if("input" in str(sampleio.text).lower() and "output" in str(sampleio.text).lower()):
            # TODO remember to check for <tt> etc within this 
            try:
                sample_input=str(sampleio.b.next_sibling).strip()+"\n"
                sample_output=str(sampleio.b.next_sibling.next_sibling.next_sibling).strip()+"\n"
                if(sample_input[0] is ":"):
                    sample_input=sample_input[1:].strip()+"\n"
                if(sample_output[0] is ":"):
                    sample_output=sample_output[1:].strip()+"\n"
                #endfix
                sample_inputs.append(sample_input)
                sample_outputs.append(sample_output)
            except:
                eprint(url,"error in case 1")
        #problem with input only or with seprate io
        elif("input" in str(sampleio.text).lower()):
            try:
                sample_input=str(sampleio.b.next_sibling).strip()+"\n"
            except:
                eprint(url,"error in case 2")
        elif("output" in str(sampleio.text).lower()):
            try:
                sample_output=str(sampleio.b.next_sibling).strip()+"\n"
            except:
                eprint(url,"error in case 3")

        elif ("input" in str(sibling).lower()):
            try:
                sample_input=sampleio.text.strip()+"\n"
                sample_inputs.append(sample_input)
            except:
                eprint(url,"error in case 3")
        elif ("output" in str(sibling).lower()):
            try:
                sample_output=sampleio.text.strip()+"\n"
                sample_outputs.append(sample_output)
            except:
               eprint(url,"error in case 3")
    
    return sample_inputs,sample_outputs

def get_problem(contest_code,problem_code):
    global problem_count
    global correct_count
    #works on the fact that sample io will be inside pre tag and if more than 1 sample than more than 1 pre tag
    url="https://www.codechef.com/api/contests/"+contest_code+"/problems/"+problem_code
    try:
        r = requests.get(url)
        j= json.loads(r.text)
        soup=BeautifulSoup(j['body'],"html.parser")
    except:
        urlerror(url)
    else:
        problem_count+=1
        pre_tag_elements=soup.find_all('pre')
        pre_tag_count=len(pre_tag_elements)
        if pre_tag_count >= 1:
            sample_inputs,sample_outputs = extract_io(pre_tag_elements,url)  
            if(len(sample_inputs)!=len(sample_outputs)):
                eprint(url,"len of sampleio not equal")
            elif(len(sample_inputs)==0 or len(sample_outputs)==0):
                eprint(url,"atleast one of input array or output array is empty")
                # handle cases for interactive problems with no input and/or no output carefully
            else:
                print("problem",problem_code,url)
                correct_count+=1
                for i in range(len(sample_inputs)):
                    print("sample input",i+1,":")
                    print(sample_inputs[i])
                    print("sample output",i+1,":")
                    print(sample_outputs[i])
        else:
            scope_err_print(url)
            problem_count-=1

    sys.stdout.flush()

'''
exceptions to above
see logs folder
'''

def get_contest(contest_code):
    url="https://www.codechef.com/api/contests/"+contest_code
    try:
        r = requests.get(url)
        j= json.loads(r.text)
    except:
        urlerror(url)
    else:
        problems=j["problems"]
        for problem in problems:
            #print(contest_code,problems[problem]["code"],problems[problem]["name"],str(problems[problem]["successful_submissions"]))
            # try:
            get_problem(contest_code,problems[problem]["code"])
        count_print(contest_code,"\tcorrect:\t",correct_count,"\tincorrect:\t",problem_count-correct_count,"\ttotal:\t",problem_count,"\tcorrect% =\t",correct_count*100//problem_count)
            # except:
                # print("error geting problem",problems[problem]["code"])


#The following function is derived from CoderCalender
#https://github.com/nishanthvijayan/CoderCalendar
#published under GNU GPL 3.0

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

#The following function is derived from CoderCalender
#https://github.com/nishanthvijayan/CoderCalendar
#published under GNU GPL 3.0
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
        # try:
        get_contest(str(details[1].a["href"][1:]))
        # except:
            # print("error get contest",str(details[1].a["href"][1:]))

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
        # try:
        get_contest(str(details[1].a["href"][1:]))
        # except:
             # print("error get contest",str(details[1].a["href"][1:]))

        #print(posts["past"])

get_contest_list()
