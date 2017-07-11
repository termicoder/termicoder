import requests
import pickle
import os

# following is the cookie file rem that it is a binary file
dir_name=os.path.dirname(__file__)
cookie_file=dir_name+"/iarcs_cookies.dump"

def save(session):
    global cookie_file
    try:
        f=open(cookie_file, 'wb')
        pickle.dump(session.cookies,file=f)
    except:
        print("error saving cookies")
        return False
    else:
        return True

def load():
    global cookie_file
    try:
        f=(open(cookie_file,'rb'))
        cookies = pickle.load(f)
        session = requests.session()
        session.cookies=cookies
    except:
        return None
    else:
        return session

def delete():
    global cookie_file
    try:
        os.remove(cookie_file)
    except:
        pass
