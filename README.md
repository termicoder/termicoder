# Termicoder

[![Build Status](https://travis-ci.org/termicoder/termicoder.svg?branch=master)](https://travis-ci.org/termicoder/termicoder)
[![PyPI](https://img.shields.io/pypi/status/termicoder.svg)](https://pypi.python.org/pypi/termicoder)
[![PyPI](https://img.shields.io/pypi/pyversions/termicoder.svg)](https://pypi.python.org/pypi/termicoder)
[![PyPI](https://img.shields.io/pypi/v/termicoder.svg)](https://pypi.python.org/pypi/termicoder)
[![Requirements Status](https://requires.io/github/termicoder/termicoder/requirements.svg?branch=master)](https://requires.io/github/termicoder/termicoder/requirements/?branch=master)
[![Licence](https://img.shields.io/github/license/termicoder/termicoder.svg)](https://github.com/termicoder/termicoder/blob/master/LICENSE.txt)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/diveshuttam)

View, Code, Submit directly from terminal  
Made with :heart: by [Divesh Uttamchandani](https://github.com/diveshuttam)

## A python based command line interface for helping in competitive programming. Termicoder aims at automating and simplifying the process of coding, testing and submitting solutions to Online Judges so that one can concentrate only on algorithms

<h3 align="center">
Inspiration behind Termicoder
</h3>
<p align="center">
  <img src="./images/inspiration.png">
</p>

## Installation

### User installation

`pip install termicoder`
use sudo -H if required. preferably use pip3 (python3)

### Developer installation

- clone this repo
- in the root folder of this repo run
  - `pip install --editable .`

notice the dot(.) in above command at the end

Note: it is better to use virtualenv and pip3 (python3)

- to remove this package, in the root folder of the repo run
  - `python setup.py develop --uninstall`

**Note: Termicoder is in its development stage and has only been tested on Ubuntu + python3. Support for other configurations is being worked on, if you are using some other platform and encounter errors, do create an [issue](https://github.com/diveshuttam/termicoder/issues) for them. For windows one can also try using [Bash on Ubuntu on Windows](https://msdn.microsoft.com/en-us/commandline/wsl/about) ; most features have been tested out there and work as expected.**

### Autocomplete for bash

To setup tab autocompletion for termicoder commands,
see `termicoder config autocomplete --help`

## Current Support

### Judges Included

1. [CodeChef](http://www.codechef.com)

### Languages Support Included

1. C
2. C++
3. Python2/3

## Highlights

```
Usage: termicoder [OPTIONS] COMMAND [ARGS]...

  __       __                      _                __
  \ \     / /____  _________ ___  (_)________  ____/ /__  _____
   \ \   / __/ _ \/ ___/ __ `__ \/ / ___/ __ \/ __  / _ \/ ___/
   / /  / /_/  __/ /  / / / / / / / /__/ /_/ / /_/ /  __/ /
  /_/   \__/\___/_/  /_/ /_/ /_/_/\___/\____/\__,_/\___/_/

  view, code & submit problems directly from terminal.

Options:
  --version            Show the version and exit.
  -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  -h, --help           Show this message and exit.

Commands:
  clip    Copies code from file to clipboard.
  code    Creates and opens file with template code.
  config  Configure settings, autocomplete etc.
  debug   Launches custom debug interface.
  list    List the contents of current folder.
  repl    Start an interactive shell.
  setup   Sets up problem, contests and login.
  submit  Submit a solution.
  test    Test code against the sample testcases.
  view    View contests and problems.
```

## Detailed Command Help

For details of a particular command use:

```bash

termicoder --help
termicoder <COMMAND> --help
```

or you can have a look at [helptext](documentation/helptext.md) which contains the output of all help commands

## Sample Run

For a sample we recommend going through [sample run](documentation/samplerun.md)
which contains the details

## ChangeLog

ChangeLog and Older Releases are availible under [Releases](https://github.com/termicoder/termicoder/releases) .

## Contributing to Termicoder

Termicoder is mostly written in python.
If you are looking towards contributing to the code base, you should begin with reading the following:

- [CONTRIBUTING](CONTRIBUTING.md)
- [GUIDELINES](documentation/guidelines.md)
- [IDEAS](https://github.com/termicoder/termicoder/blob/master/documentation/ideas.md).

You can also contribute otherwise by

- Improving the Documentation.
  - Most of the documentation lies in the [documentation](https://github.com/termicoder/termicoder/tree/master/documentation) folder. To start fork this repo, change and create a pull request

- reporting a bug or requesting a feature.
  - Please create an [issue](https://github.com/termicoder/termicoder/issues) about the bug/feature.

- Giving feedback about the work. (both praise and criticism are equally appreciated).
  - mail : diveshuttamchandani@gmail.com

## LICENSE

[MIT](LICENSE.txt)
