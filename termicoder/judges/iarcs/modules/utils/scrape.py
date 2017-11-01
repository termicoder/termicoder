import requests
from bs4 import BeautifulSoup
import sys
import termicoder.judges.iarcs.modules.utils.session as session
import termicoder.utils.display as display


def get_problem_list():
    iarcs_session = session.iarcs_session
    logged_in = (session.is_logged_in())
    url = "http://opc.iarcs.org.in/index.php/problems/"
    try:
        r = iarcs_session.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
    except BaseException:
        display.url_error(url, abort=True)
    else:
        unsolved_list = []
        problem_rows = soup.find_all("tr")[1:-1]    # 0th row contains heading
        for problem in problem_rows:
            row_data = problem.find_all("td")
            code_data, problem_data = row_data[1], row_data[2]
            status = None
            if(logged_in):
                status = row_data[3].text
            if(not status):
                unsolved_list.append({"problem_code": code_data.a.text,
                                      "problem_name": problem_data.a.text})
        return unsolved_list


def extract_io(iocandidate):
    sample_io = []
    sample_inputs = []
    sample_outputs = []
    for candidate in iocandidate:
        sibling = candidate.previous_sibling
        while(not str(sibling).strip()):
            sibling = sibling.previous_sibling
        if("sample" in str(sibling).lower()):
            sample_io.append(candidate)

    for i in range(len(sample_io)//2):
        sample_input = sample_io[2*i].get_text(strip=True)+"\n"
        sample_inputs.append(sample_input)
        # added a \n at the end as initially stripped

        sample_output = sample_io[2*i+1].get_text(strip=True)+"\n"
        sample_outputs.append(sample_output)
        # added a \n at the end as initially stripped
    return sample_inputs, sample_outputs


def get_problem(problem_code, abort_on_error=False):
    url = "http://opc.iarcs.org.in/index.php/problems/" + problem_code
    j = {"error": None,
         "judge": "iarcs",
         "problem_code": problem_code}
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        display.check_response_status(r, abort=abort_on_error)
    except SystemExit:
        sys.exit()
    except BaseException:
        display.url_error(url, abort=abort_on_error)
        j["error"] = "urlerror"
    else:
        j["body"] = str(soup.find(id='maincontent'))
        iocandidate = soup.find_all("pre")
        sample_inputs, sample_outputs = extract_io(iocandidate)
        sample_io = {}
        sample_io["inputs"] = sample_inputs
        sample_io["outputs"] = sample_outputs
        if(len(sample_inputs) == len(sample_outputs)):
            sample_io["error"] = None
        else:
            sample_io["error"] = "sample io not equal"
        j["sample_io"] = sample_io
        return j
