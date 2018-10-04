#!/usr/bin/python
# -*- coding: utf-8 -*-

# ABC is the AbstractBaseClass in python
from abc import ABC, abstractmethod


class Contest(ABC):
    @abstractmethod
    def __init__(self, data=None):
        # If contest_data, problems is passed, it should take priority
        self.code = None
        self.problems = None
        self.judge_name = None
        self.data = data

    @abstractmethod
    def __str__(self):
        pass
