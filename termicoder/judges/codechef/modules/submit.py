import requests
import os
import termicoder.judges.codechef.modules.utils.session as session
import time

def submit(problem_code,contest_code,solution_path,language_code):
    codechef_session=session.codechef_session
    if(session.is_logged_in()==False):
        display.error("You are not logged in")
        return None
    else:
        # TODO check if it is able to submit(allowed)
        try:
            solution_text=open(solution_path,'r').read()
        except:
            display.error("The solution file could not be loaded")
            return None
        submit_url="https://www.codechef.com/api/ide/submit"
        submit_data={
        "sourceCode":solution_text,
        "problemCode":problem_code,
        "contestCode":contest_code,
        "language":language_code
        }
        a=codechef_session.post(submit_url,data=submit_data)
        if(a.status_code==200):
            return a.json()
        else:
            return None



def check_status(upid):
    codechef_session=session.codechef_session
    check_url="https://www.codechef.com/api/ide/submit"
    payload={"solution_id":upid}
    a=codechef_session.get(check_url,params=payload).json()
    return a

"""
a trial main function to test submit
"""
if __name__ == "__main__":
    wait_time=1
    session.load(force_login=True)
    a=submit("TEST","PRACTICE","./test.cpp",44)
    print(a)
    print("checking status")
    b=check_status(a["upid"])
    #I suspect that it can be infinite loop
    while(b is not None and b["result_code"]=='wait'):
        print(b)
        b=check_status(a["upid"])
        time.sleep(wait_time)
    print(b)
