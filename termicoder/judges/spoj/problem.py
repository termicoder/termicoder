'''
cd to folder
usage: python spoj.py [url of problem]
'''

import requests
import sys
import textwrap
from bs4 import BeautifulSoup


def problem(url):
    r = requests.get(url)
    if r.status_code == 404:
        sys.exit("please check the problem code you entered")
    else:
        soup = BeautifulSoup(r.text, "html.parser")
        print soup.find('h1#problem-name').text
        print
        body = soup.select('div#problem-body')[0].text
        if body.find('Input') < body.find('Example'):
            in_index, out_index, info_index, eg_index = body.find('Input'), body.find(
                'Output'), body.find('Information'), body.find('Example')
            print textwrap.fill(body[0:in_index], width=80)
            print
            print 'Input'
            print textwrap.fill(body[in_index+5:out_index], width=80)
            print
            print 'Output'
            print textwrap.fill(body[out_index+6: eg_index], width=80)
            print
            if info_index != -1:
                print body[eg_index:info_index]
            else:
                print body[eg_index::1]
        else:
            eg_index, info_index = body.find(
                'Example'), body.find('Information')
            print textwrap.fill(body[0:eg_index], width=80)
            print
            if info_index != -1:
                print body[eg_index:info_index]
            else:
                print body[eg_index::1]


if __name__ == "__main__":
    problem(sys.argv[1])
