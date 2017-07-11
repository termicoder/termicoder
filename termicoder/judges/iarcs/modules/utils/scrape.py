import click
import requests
from bs4 import BeautifulSoup
import re
import sys
import termicoder.judges.iarcs.modules.utils.session as session
import termicoder.utils.display as display

def get_problem_list():
    iarcs_session=session.iarcs_session
    logged_in=(session.is_logged_in())
    url = "http://opc.iarcs.org.in/index.php/problems/"
    try:
        r = iarcs_session.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
    except:
        display.url_error(url,abort=True)
    else:
        assume_error=False
        unsolved_list = []
        problem_rows = soup.find_all("tr")[1:-1]    # 0th row contains heading
        for problem in problem_rows:
            row_data = problem.find_all("td")
            code_data, problem_data = row_data[1], row_data[2]
            status=None
            if(logged_in):
                status=row_data[3].text
            if(not status):
                unsolved_list.append({"problem_code":code_data.a.text,
                                    "problem_name":problem_data.a.text})
        return unsolved_list


def get_problem(problem_code):
    # <pre class="c3">
    url = "http://opc.iarcs.org.in/index.php/problems/" + problem_code
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
    except:
        print("error fetching url:"+url)
    else:
        sample_io=[]
        iocandidate = soup.find_all("pre")
        for candidate in iocandidate:
            #print("prev")
            sibling = candidate.previous_sibling
            while(not str(sibling).strip()):
                sibling=sibling.previous_sibling
            if("sample" in str(sibling).lower()):
                sample_io.append(candidate)
        print(problem_code,url)
        if(len(sample_io)%2 == 1):
            print("error len=",len(sample_io))
        else:
            for i in range(len(sample_io)//2):
                sample_input=sample_io[2*i].get_text(strip=True)+"\n"       # added a \n at the end as initially stripped
                sample_output=sample_io[2*i+1].get_text(strip=True)+"\n"    # added a \n at the end as initially stripped
                print("Sample Input",i+1)
                print(sample_input)
                print("Sample Output",i+1)
                print(sample_output)
        print("----------------------------------------------------------------")
        sys.stdout.flush()
