#!/usr/bin/python
# -*- coding: utf-8 -*-

# ABC is the AbstractBaseClass in python
from abc import ABC, abstractmethod


class Tag:
    def __init__(self):
        self.id = None
        self.display_name = None
        self.synonyms = None
