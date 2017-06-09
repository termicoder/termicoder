import requests
from bs4 import BeautifulSoup
import json

def problems(contest_code,problem_code):
    url="https://www.codechef.com/api/contests/"+contest_code+"/problems/"+problem_code
    try:
        r = requests.get(url)
        j= json.loads(r.text)
        soup=BeautifulSoup(j['body'],"html.parser")
    except:
         print("error in fetching url:\n" + url)
    else:
        #loop because there can be others pre in a problem example https://www.codechef.com/JUNE17/problems/PRMQ
        for sampleio in soup.find_all('pre'):
            try:    
                sample_input=str(sampleio.b.next_sibling).strip()+"\n"
                sample_output=str(sampleio.b.next_sibling.next_sibling.next_sibling).strip()+"\n"

                #fix for problem https://www.codechef.com/JUNE17/problems/XENRANK
                if(sample_input[0] is ":"):
                    sample_input=sample_input[1:].strip()+"\n"
                if(sample_output[0] is ":"):
                    sample_output=sample_output[1:].strip()+"\n"
                #endfix
                    
                print(sample_input)
                print(sample_output)
            except:
                #TODO create a log of the exception
                continue



def contest(contest_code):
    url="https://www.codechef.com/api/contests/"+contest_code
    try:
        r = requests.get(url)
        j= json.loads(r.text)
    except:
        print("error in fetching url:\n" + url)
    else:
        problems=j["problems"]
        for problem in problems:
            print(problems[problem]["code"]+" "+problems[problem]["name"]+" "+problems[problem]["successful_submissions"])
