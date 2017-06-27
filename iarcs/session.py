import requests
from bs4 import BeautifulSoup
import getpass
import pprint

url="http://opc.iarcs.org.in/index.php"
iarcs_session=requests.session()
verbose=True

def if_verbose_print(*args, **kwargs):
    if 'verbose' in globals() and verbose == True:
        print(*args, **kwargs)

# this function is significantly general for filling forms
# try to make it more general
def login():
    login_url=url+"/auth/login"
    global iarcs_session
    login_page=iarcs_session.get(login_url)
    if_verbose_print("got the login page")
    form_feilds=BeautifulSoup(login_page.text,"html.parser").findAll("input")
    form_data={}

    for i in form_feilds:
        attrs=i.attrs
        print(i)
        if "name" in attrs:
            if "value" in attrs and attrs["value"]:
                form_data[attrs["name"]]=attrs["value"]
            else:
                if "type" in attrs:
                    if_verbose_print("Field type:",str(attrs["type"]).lower())
                    if str(attrs["type"]).lower() == "password":
                        form_data[attrs["name"]]=getpass.getpass("Enter "+ attrs["name"] +": ")

                if attrs["name"] not in form_data:
                    form_data[attrs["name"]]=input("Enter " + attrs["name"] +": ")

    if_verbose_print("The following is the form data that will be sent:\n",\
                     pprint.pformat(form_data,indent=2))
    print("logging you into iarcs... please wait...")
    global logged_page
    logged_page=iarcs_session.post(login_url,form_data)

def logout():
	global iarcs_session
	logout_url=url+"/auth/logout"
	a=iarcs_session.get(logout_url)
	print(a.text)
