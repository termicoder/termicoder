#!/usr/bin/python
# -*- coding: utf-8 -*-
from termicoder.models import Contest
from collections import namedtuple
from beautifultable import BeautifulTable
from termicoder.utils.logging import logger


class CodechefContest(Contest):
    def __init__(self, data):
        self.code = None
        self.problems = []
        self.data = data
        self.judge_name = "codechef"
        self.problem_codes = []
        if(data is not None):
            self._initialize()

    def _initialize(self):
        concerned_data = self.data['result']['data']['content']
        content = namedtuple(
            "problem", concerned_data.keys())(*concerned_data.values())
        self.code = content.code
        self.problem_codes = [x['problemCode'] for x in content.problemsList]

    def __str__(self):
        problems = self.problems
        table = BeautifulTable()
        table.width_exceed_policy = BeautifulTable.WEP_WRAP
        # TODO: use map style.headers instead of str
        # requires change with beautifultable. we may try dev version
        # TODO: sort with submission
        # TODO add status with color code (AC, WA .. etc)
        table.column_headers = list(
            map(str, ['code', 'name', 'submissions']))
        for problem in problems:
            table.append_row(
                [
                    problem.code, problem.name, problem.submissions_count
                ]
            )
        return str(table)
