#!/usr/bin/python
# -*- coding: utf-8 -*-

# ABC is the AbstractBaseClass in python
from abc import ABC, abstractmethod
from ..utils import icdiff


class Testcase(ABC):
    @abstractmethod
    def __init__(self, ans, inp, code):
        self.ans = ans
        self.inp = inp
        self.code = code

    # judges can override this if they want
    # this is used to produce diff on termicoder test
    def diff(self, out):
        ans_file_name = self.code + ".ans"
        out_file_name = self.code + ".out"
        ans_list = [x+'\n' for x in self.ans.split('\n')]
        out_list = [x+'\n' for x in out.split('\n')]
        diffobj = icdiff.ConsoleDiff(line_numbers=True, show_all_spaces=True)

        if(ans_list == out_list):
            return None
        else:
            return '\n'.join(diffobj.make_table(
                             out_list, ans_list, fromdesc=out_file_name,
                             todesc=ans_file_name, context=False, numlines=10))
