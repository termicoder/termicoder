from termicoder.models import Problem
from termicoder.utils.logging import logger
from collections import namedtuple
import markdown
import os
from ..utils.testcases import extract
from tomd import Tomd
import mdv


class CodechefProblem(Problem):
    def __init__(self, data=None):
        self.code = None
        self.data = data
        self.html = None
        self.name = None
        self.status = None
        self.submission_count = 0
        self.testcases = None
        self.judge_name = "codechef"
        self.timelimit = 3.0
        if(data is not None):
            self._initialize()

    def _initialize(self):
        concerned_data = self.data['result']['data']['content']
        problem_content = namedtuple(
            "problem", concerned_data.keys())(*concerned_data.values())
        self.name = problem_content.problemName
        self.submissions_count = problem_content.successfulSubmissions
        self.code = problem_content.problemCode
        self.text = problem_content.body
        self.html = self._get_html(problem_content.body)
        self.testcases = self._extract_testcases(self.html)
        self.timelimit = problem_content.maxTimeLimit

    def _get_html(self, body):
        newbody = body.replace('<br>', '\n')
        newbody = newbody.replace('<br />', '\n')
        self.text = newbody
        mdProcessor = markdown.Markdown()
        myHtmlFragment = str(mdProcessor.convert(newbody))
        myHtmlFragment = myHtmlFragment.replace('<code>', '<pre>')
        myHtmlFragment = myHtmlFragment.replace('</code>', '</pre>')
        logger.debug(myHtmlFragment)
        javascript = open(
            os.path.join((os.path.dirname(__file__)), "script.js")).read()
        return ("<script>%s</script>" % javascript) + myHtmlFragment

    def _extract_testcases(self, html):
        testcases = extract(html)
        return testcases

    def __str__(self):
        ret = self.text
        ret = ret.replace('_', '')
        keymap = {
            r'\le': r"<=",
            r'\cdot': r".",
            r'\ge': r">=",
            r'\lt': r"<",
            r'$': r"_",
            r'\dots': r"..."
        }
        for key in keymap:
            value = keymap[key]
            ret = ret.replace(key, value)

        # temprorily convert to html
        mdProcessor = markdown.Markdown()
        myHtmlFragment = str(mdProcessor.convert(ret))
        myHtmlFragment = myHtmlFragment.replace('<code>', r"```")
        myHtmlFragment = myHtmlFragment.replace('</code>', r"```")

        ret = Tomd(myHtmlFragment).markdown

        # calling like this (all CLI options supported, check def main
        ret = mdv.main(ret)
        return ret
