'''
cd to folder
usage: python spoj.py [url of problem]
'''

import requests, sys, textwrap
from bs4 import BeautifulSoup


def problem(url):
    r = requests.get(url)
    if r.status_code == 404:
        sys.exit("please check the problem code you entered")
    else:
        soup = BeautifulSoup(r.text, "html.parser")
        print soup.select('h2#problem-name')[0].text
        print
        body = soup.select('div#problem-body')[0].text
        index = min(body.find('Example'), body.find('Input'), body.find('Output'))
        print textwrap.fill(body[0:index], width=80)
        print
        print body[index::1]

problem(sys.argv[1])