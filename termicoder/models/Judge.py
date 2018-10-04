#!/usr/bin/python
# -*- coding: utf-8 -*-

# ABC is the AbstractBaseClass in python
from abc import ABC, abstractmethod


# Judge is an abstract class to be subclassed and implemented
# by Judge developers.

# Judge class kind of doubles up for login-logout as well as a Factory
# for the contest and problem classes for the particular judge
class Judge(ABC):
    @abstractmethod
    def __init__(self, session_data=None):
        # Init should not have any network requests
        # do them in login, logout, check_running_contest
        self.session_data = session_data

    @abstractmethod
    def check_login(self):
        pass

    @abstractmethod
    def login(self):
        # login also controls all the messages being displayed to the user
        pass

    @abstractmethod
    def logout(self):
        # logout also controls all the messages displayed to the user
        pass

    @abstractmethod
    def get_running_contests(self):
        # return a string of running contest, do it in form of a table.
        pass

    # This method serves both as a problem getter as well as kind of factory
    # for problem
    @abstractmethod
    def get_problem(self, problem_code, contest_code):
        # Method should call the respective Problem.__init__ method to create a
        # problem instance and return it
        pass

    @abstractmethod
    def get_contest(self, contest_code):
        # Method should call the respective Problem.__init__ method to create a
        # contest instance with all its problems and return it
        pass

    @abstractmethod
    def get_problem_url(self, problem_code, contest_code):
        # Method should return the url used by judge for a particular problem
        pass

    @abstractmethod
    def get_contest_url(self, contest_code):
        # Method should return the url used by judge for a particular contest
        pass

    @abstractmethod
    def get_contests_list_url(self):
        # Method should return the url used by judge for listing contest
        pass

    @abstractmethod
    def submit(self, problem, code_text, extension):
        # problem is an instance of judge's problem class
        # code test is the code to be submitted
        # extension is the extension of the code file to determine
        # language of submission
        pass

    @abstractmethod
    def get_testcase(self, inp, ans, code):
        # returns the testcase with inp, ans and code
        # used by termicoder test to output diff
        pass
