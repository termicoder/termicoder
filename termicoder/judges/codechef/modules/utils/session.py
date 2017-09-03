import click
import requests
from bs4 import BeautifulSoup
import termicoder.utils.style
import time
from termicoder.judges.codechef.modules.utils import cookies
from termicoder.utils import display
from termicoder.utils import style

url="https://www.codechef.com"
codechef_session=requests.session()

def login(username,password):
    global codechef_session
    login_url=url+"/"
    try:
        login_page=codechef_session.get(login_url)
    except:
        display.url_error(login_url,abort=True)

    form_feilds=BeautifulSoup(login_page.text,"html.parser").findAll("input")

    form_data={"pass":password,
    "name":username}

    for i in form_feilds:
        attrs=i.attrs
        if "name" in attrs:
            if "value" in attrs and attrs["value"]:
                form_data[attrs["name"]]=attrs["value"]
    try:
        logged_page=codechef_session.post(login_url,form_data)
    except:
        display.url_error(login_url,abort=True)
    else:
        # logout all other sessions as codechef doesn't allows multiple sessions
        if("session/limit" in logged_page.url):
            click.confirm("Session limit exceeded\n"+
            "Do you want to logout of other sessions",
            default=True,abort=True)
            display.normal("logging you out of all other sessions\n"+
            "this may take some time...")
        while "session/limit" in logged_page.url:
            logout_other_session()
            logged_page=codechef_session.post(url,form_data)

        # codechef doesn't check cookies and trivially displays the latest as current session
        # handle this using modifying logout_other_session by logging out after checking session cookies
        # and matching with form data. trivially the following solution works

        logged_page=codechef_session.post(url,form_data)
        if len(BeautifulSoup(logged_page.text,"html.parser").findAll("input"))>0 and is_logged_in(ensure=True)==True:
            click.confirm(style.error("You are/have tried to login to codechef while"+
            "the script was running\nDo you want to try login again?"),default=True,
            abort=True)
            login(username,password)
        else:
            if(is_logged_in(ensure=True) == True):
                if(cookies.save(codechef_session)==True):
                    return True
            else:
                display.credential_error("codechef",abort=True)


def logout_other_session():
    global codechef_session
    sess_url=url+"/session/limit"
    try:
        session_page=codechef_session.get(sess_url)
    except:
        display.url_error(sess_url,abort=True)

    form_feilds=BeautifulSoup(session_page.text,"html.parser").findAll("input")
    form_data={}
    for j in [0,-1,-2,-3,-4]:
        i=form_feilds[j]
        attrs=i.attrs
        if "name" in attrs:
            if "value" in attrs and attrs["value"]:
                form_data[attrs["name"]]=attrs["value"]
    try:
        a=codechef_session.post(sess_url,data=form_data)
    except:
        display.url_error(sess_url,abort=True)

def logout():
    global codechef_session
    logout_url=url+"/logout"
    try:
        a=codechef_session.get(logout_url)
    except:
        display.url_error(logout_url,abort=True)
    else:
        if(cookies.delete()==True):
            return True
        else:
            return None

def load(force_login=False):
    global codechef_session
    session=cookies.load()
    if(session!=None):
        codechef_session=session
    elif(force_login):
        login()

def is_logged_in(ensure=True):
    global codechef_session
    user_url="https://www.codechef.com/api/user/me"
    if(ensure==True):
        try:
            page=codechef_session.get(user_url).json()
        except:
            return None
        if(page["user"]["username"]==None):
            return False
        else:
            return True
    else:
        if(cookies.load()== None):
            return False
        else:
            return True
