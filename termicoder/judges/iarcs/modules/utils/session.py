import requests
from bs4 import BeautifulSoup,Comment
import getpass
import termicoder.judges.iarcs.modules.utils.cookies as cookies
import termicoder.utils.display as display

url="http://opc.iarcs.org.in/"
iarcs_session=requests.session()
#None=> urlerror
#True=> logged in
#False=> user error
def login(username,password):
    login_url=url+"index.php/auth/login"
    global iarcs_session
    form_data={
    "username":username,
    "password":password,
    "redirectto":"/"
    }
    try:
        logged_page=iarcs_session.post(login_url,form_data)
    except:
        display.url_error(login_url,abort=True)
    else:
        if(is_logged_in(ensure=True,passed_page=logged_page) == True):
            if(cookies.save(iarcs_session)==True):
                return True
        else:
            display.credential_error("iarcs",abort=True)

def logout():
    global iarcs_session
    logout_url=url+"index.php/auth/logout"
    try:
        a=iarcs_session.get(logout_url)
    except:
        display.url_error(logout_url,abort=True)
    else:
        if(cookies.delete()==True):
            return True
        else:
            return None

def load(force_login=False):
    global iarcs_session
    session = cookies.load()
    if(session):
        iarcs_session=session
    elif (force_login):
        login()

def is_logged_in(ensure=True,passed_page=None):
    global iarcs_session
    if(ensure==True):
        if(passed_page):
            page=passed_page
        else:
            try:
                page=iarcs_session.get(url+"index.php")
            except:
                return None
        soup=BeautifulSoup(page.text,'html.parser')
        user_str=soup.find(text=lambda text:isinstance(text, Comment)).strip()
        if(len(user_str)>5):
            return True
        else:
            return False
    else:
        if(cookies.load()== None):
            return False
        else:
            return True
