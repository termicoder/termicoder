import requests, pickle

# name of cookie file rem that it is a binary file

cookie_file="cookies"

def save_cookies():
    with open(cookie_file, 'wb') as f:
        print(session.cookies)
        pickle.dump(session.cookies,file=f)

def load_session_with_cookies():
    with open(cookie_file,'rb') as f:
        cookies = pickle.load(f)
        session = requests.session()
        session.cookies=cookies
        print(session.cookies)
        return session
