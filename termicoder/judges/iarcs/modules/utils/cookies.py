import requests, pickle

# following is the cookie file rem that it is a binary file
cookie_file="iarcs_cookies.dump"

def save_cookies(session):
    global cookie_file
    with open(cookie_file, 'wb') as f:
        print(session.cookies)
        pickle.dump(session.cookies,file=f)

def load_cookies():
    global cookie_file
    try:
        f=(open(cookie_file,'rb')
        cookies = pickle.load(f)
        session = requests.session()
        session.cookies=cookies
    except:
        return None
    else:
        return session
