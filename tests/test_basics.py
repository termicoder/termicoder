#!/usr/bin/env python
import unittest
from click.testing import CliRunner

import termicoder.cli


class test_cli_help(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_initial(self):
        result = self.runner.invoke(termicoder.cli.main, ['--help'])
        assert result.exit_code == 0
