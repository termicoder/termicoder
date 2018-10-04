#!/usr/bin/python
# -*- coding: utf-8 -*-

# ABC is the AbstractBaseClass in python
from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self):
        self.judge = None
        self.username = None
        self.settings = None
        self.token = None
