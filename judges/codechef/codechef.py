import requests
from bs4 import BeautifulSoup
import json
from time import strptime,strftime,mktime,gmtime,localtime
import sys
import os

def sanitize(io):
    """
    this funtion removes ":" "1:" etc if any in front of the io
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
    sample_inputs=[]
    sample_outputs=[]
    for sampleio in pre_tag_elements:
        # finding heading / previous sibling of pre
        sibling = sampleio.previous_sibling
        while(not str(sibling).strip()):
            sibling = sibling.previous_sibling

        # converting sampleio to text
        iotext=str(sampleio.text)

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
        elif("input" in str(sampleio.text).lower() or "input" in str(sibling).lower()):
            in_index = iotext.lower().find("input")
            ki=1 if (in_index == -1) else 5
            sample_input = sanitize(iotext[in_index+ki:])
            sample_inputs.append(sample_input)

        # problem with output only like printing 100! etc
        # or input and output in seperate pre tags
        elif("output" in str(sampleio.text).lower() or "output" in str(sibling).lower()):
            out_index = iotext.lower().find("output")
            ko=1 if (out_index == -1) else 6
            sample_output = sanitize(iotext[out_index+ko:])
            sample_outputs.append(sample_output)

    return sample_inputs,sample_outputs

def get_problem(contest_code,problem_code):
    # works on the fact that sample io will be inside pre tag and if more than 1 sample than more than 1 pre tag
    url="https://www.codechef.com/api/contests/"+contest_code+"/problems/"+problem_code
    try:
        r = requests.get(url)
        j= json.loads(r.text)
        soup=BeautifulSoup(j['body'],"html.parser")
    except:
        print("error in fetching",url)
    else:
        pre_tag_elements=soup.find_all('pre')
        pre_tag_count=len(pre_tag_elements)
        sampleio={}
        if pre_tag_count >= 1:
            sample_inputs,sample_outputs = extract_io(pre_tag_elements,url)
            sampleio["inputs"]=sample_inputs
            sampleio["outputs"]=sample_outputs
            sampleio["error"]=""
        else:
            sampleio["error"]="Out of Scope"
        j["sampleio"]=sampleio
        j["judge"]="codechef"
        return j

def get_contest(contest_code):
    url="https://www.codechef.com/api/contests/"+contest_code
    try:
        r = requests.get(url)
        j= json.loads(r.text)
    except:
        print("error in fetching",url)
        raise "FetchError"
    else:
        j["judge"]="codechef"
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
    url="http://www.codechef.com/contests"
    page = requests.get(url)
    print("got the list")
    soup = BeautifulSoup(page.text, "html.parser")

    contest_tables = {"Future Contests": [], "Present Contests": [],"Past Contests":[]}
    contests= {"ongoing":[] , "upcoming":[], "past":[]}
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

def setup_problem(contest_code,problem_code):
    problem_path=os.path.join(".",contest_code,problem_code)
    try:
        os.mkdir(problem_path)
    except:
        pass
    problem=get_problem(contest_code,problem_code)

    problem_html=problem["body"]
    del problem["body"]
    sampleio=problem["sampleio"]
    del problem["sampleio"]

    # the problem data
    problem_setup_file=os.path.join(problem_path,".problem")
    f1=open(problem_setup_file,"w")
    print(json.dumps(problem,indent=2,sort_keys=True),file=f1)

    # html problem statement
    problem_html_file=os.path.join(problem_path,problem_code+".html")
    f2=open(problem_html_file,"w")
    print(problem_html,file=f2)

    # sampleio files
    if(sampleio["error"]==""):
        testcases_path=os.path.join(problem_path,"testcases")
        try:
            os.mkdir(testcases_path)
        except:
            pass
        for i in range(len(sampleio["inputs"])):
            input_file=os.path.join(testcases_path,str(i+1)+".in")
            ifile=open(input_file,"w")
            print(sampleio["inputs"][i],file=ifile)
        for o in range(len(sampleio["outputs"])):
            output_file=os.path.join(testcases_path,str(o+1)+".out")
            ofile=open(output_file,"w")
            print(sampleio["outputs"][o],file=ofile)

    
def setup_contest(contest_code):
    contest_path=os.path.join(".",contest_code)
    try:
        os.mkdir(contest_path)
    except:
        pass
    contest_setup_file=os.path.join(contest_path,".contest")
    f=open(contest_setup_file,"w")
    contest=get_contest(contest_code)
    del contest["rules"]
    print(json.dumps(contest,indent=2),file=f)

    for problem_code in contest["problems"]:
        setup_problem(contest_code,problem_code)
    
    

if(__name__=="__main__"):
    # trial contest setup in current dir
    setup_contest("JUNE17")
