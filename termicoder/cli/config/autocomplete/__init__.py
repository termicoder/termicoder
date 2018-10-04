#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import click

import click_completion
import click_completion.core

from . import install
from . import show


def custom_startswith(string, incomplete):
    """A custom completion matching that supports case insensitive matching"""
    if os.environ.get('_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE'):
        string = string.lower()
        incomplete = incomplete.lower()
    return string.startswith(incomplete)


click_completion.core.startswith = custom_startswith
click_completion.init()


cmd_help = """Shell completion for termicoder.

Available shell types:

\b
  %s
Default type: auto
""" % "\n  ".join('{:<12} {}'.format(k,
                  click_completion.core.shells[k]) for k in sorted(
    click_completion.core.shells.keys()))


@click.group(help=cmd_help)
def main():
    pass


sub_commands = [
    {
        "cmd": install.main,
        "name": "install"
    },
    {
        "cmd": show.main,
        "name": "show"
    }
]

for command in sub_commands:
    main.add_command(**command)

__all__ = ['main']
