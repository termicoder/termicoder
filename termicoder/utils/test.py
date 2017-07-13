import click
import os
import sys
import termicoder.utils.display as display
import termicoder.utils.parse as parse

lang_map={
".py":"python",
".java":"gcj",
".c":"c",
".cpp":"cpp",
".cc":"cpp",
".c++":"cpp"
}

def test(code_file):
    """
    simulates oj test sort of
    """
    # code file will exist thanks to click
    # define online judge constant
    display.normal("test not implemented yet")
    f=open(code_file,"r")
    testcase_path=("testcase")
    time_limit = parse.get_time_limit()
    memory_limit = parse.get_memory_limit()

    stats={
    "max_time":0.00,
    "memory":0.00,
    "status":None
    }
    status={
    "ce":"compilation error",
    "ac":"correct",
    "wa":"wrong ans",
    "rte":"runtime error"
    }
