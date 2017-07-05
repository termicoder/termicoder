import requests
import pickle
import os

# name of cookie file rem that it is a binary file
cookie_file="codechefcookies.dump"

def save(session):
    with open(cookie_file, 'wb') as f:
        pickle.dump(session.cookies,file=f)

def load_session():
    try:
        f=open(cookie_file,'rb')
    except:
        return None
    else:
        cookies = pickle.load(f)
        session = requests.session()
        session.cookies=cookies
        return session

def delete():
    try:
        f=open(cookie_file,'wb')
        os.remove(cookie_file)
    except:
        pass
        

