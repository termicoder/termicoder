# Termicoder  
[![Build Status](https://travis-ci.org/termicoder/termicoder.svg?branch=master)](https://travis-ci.org/termicoder/termicoder)
[![PyPI](https://img.shields.io/pypi/status/termicoder.svg)](https://pypi.python.org/pypi/termicoder)
[![PyPI](https://img.shields.io/pypi/pyversions/termicoder.svg)](https://pypi.python.org/pypi/termicoder)
[![PyPI](https://img.shields.io/pypi/v/termicoder.svg)](https://pypi.python.org/pypi/termicoder)
[![Requirements Status](https://requires.io/github/termicoder/termicoder/requirements.svg?branch=master)](https://requires.io/github/termicoder/termicoder/requirements/?branch=master)
[![Licence](https://img.shields.io/github/license/termicoder/termicoder.svg)](https://github.com/termicoder/termicoder/blob/master/LICENSE.txt)



View, Code, Submit directly from terminal  
Made with :heart: by [Divesh Uttamchandani](https://github.com/diveshuttam)  
  
### A python based command line interface for helping in competitive programming. Termicoder aims at automating and simplifying the process of coding, testing and submitting problems to Online Judges so that one can concentrate only on algorithms    

## Installation

### User installation
`pip install termicoder`  
use sudo -H if required. preferably use pip3 (python3)

### Developer installation  
- clone this repo  
- in the root folder of this repo run  
`pip install --editable . `  
notice the dot(.) in above command at the end   
  
Note: it is better to use virtualenv and pip3 (python3)  

- to remove this package, in the root folder of the repo run  
`python setup.py develop --uninstall`

**Note: Termicoder is in its alpha stage and has only been tested on Ubuntu + python3. Support for other configurations is being worked on, if you are using some other platform and encounter errors, do create an [issue](https://github.com/diveshuttam/termicoder/issues) for them. For windows one can also try using [Bash on Ubuntu on Windows](https://msdn.microsoft.com/en-us/commandline/wsl/about) ; most features have been tested out there and work as expected.**
  

### Autocomplete for bash  
To setup tab autocompetion for termicoder commands have a look at [Autocomplete Setup](documentation/autocomplete.md).

## Current Support

### Judges Supported Currently:
1. [Iarcs Opc](http://opc.iarcs.org.in/index.php/)  
2. [CodeChef](http://www.codechef.com)

### Languages Supported Currently:
1. C  
2. C++  
3. Python2/3
4. Java (is still being worked on)

## Highlights
```
Usage: termicoder [OPTIONS] COMMAND [ARGS]...

  view, code & submit problems directly from terminal.

Commands:
  code    creates file with template code.  
  setup   sets up problem, contests and login.  
  submit  submit a solution.  
  test    test code against the sample testcases.  
  view    view contests, problems and problem statement
```

## Detailed Command Help
For details of a particular command use:  

```
termicoder --help  
termicoder <COMMAND> --help  
```  

or you can have a look at [helptext](documentation/helptext.md) which contains the output of all help commands

## Sample Run 
For a sample we reccommend going through [sample run](documentation/samplerun.md)
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
* Improving the Documentation.
  - Most of the documentation lies in the [documentation](https://github.com/termicoder/termicoder/tree/master/documentation) folder. To start fork this repo, change and create a pull request
  
* reporting a bug or requesting a feature.
  - Please create an [issue](https://github.com/termicoder/termicoder/issues) about the bug/feature.

* Giving feedback about the work. (both praise and criticism are equally appreciated).
  - mail : diveshuttamchandani@gmail.com


## LICENSE
[MIT](LICENSE.txt)
