#!/usr/bin/python
# -*- coding: utf-8 -*-

# ABC is the AbstractBaseClass in python
from abc import ABC, abstractmethod


class Problem(ABC):
    @abstractmethod
    def __init__(self, data):
        self.name = None
        self.status = None
        self.submissions_count = 0
        self.data = data
        self.code = None
        self.html = None
        self.testcases = None
        self.contest_code = None
        self.judge_name = None
        self.timelimit = 3.0  # in seconds

    # used by list
    @abstractmethod
    def __str__(self):
        pass
