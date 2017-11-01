import requests
import pickle
import os
import termicoder.utils.display as display
# following is the cookie file rem that it is a binary file
dir_name = os.path.dirname(__file__)
cookie_file_path = dir_name+"/codechef_cookies.dump"


def save(session):
    global cookie_file_path
    try:
        f = open(cookie_file_path, 'wb')
        pickle.dump(session.cookies, file=f)
    except BaseException:
        display.file_save_error(cookie_file_path, abort=True)
        return False
    else:
        return True


def load():
    global cookie_file_path
    try:
        f = (open(cookie_file_path, 'rb'))
        cookies = pickle.load(f)
        session = requests.session()
        session.cookies = cookies
    except BaseException:
        return None
    else:
        return session


def delete():
    global cookie_file_path
    try:
        os.remove(cookie_file_path)
    except BaseException:
        return False
    else:
        return True
