==========
Termicoder
==========


View, Code, Submit directly from terminal
Made with :heart: by Divesh Uttamchandani

Installation

User installation

pip install termicoder
use sudo -H if required. preferably use pip3 (python3)

Developer installation

clone this repo
in the root folder of this repo run
pip install --editable .
notice the dot(.) in above command at the end
Note: it is better to use virtualenv and pip3 (python3)

Autocomplete for bash

Method 1:
run the following command every time you use terminal
eval "$(_TERMICODER_COMPLETE=source termicoder)"

Method 2:
put the following command in your .bashrc
eval "$(_TERMICODER_COMPLETE=source termicoder)"

Method 3:
Method 2 makes bash to load up slowly, so try:
eval "$(_TERMICODER_COMPLETE=source termicoder)" > autocomplete.sh
and put . path_to_autocompte.sh/autocomplete.sh in your .bashrc

Current Support

Judges Supported Currently:

Iarcs Opc
CodeChef
Languages Supported Currently:

C
C++
Java
Python2/3
Usage

Only basic usage highlighted here,
for details of a particular command use:

termicoder --help  
termicoder <COMMAND> --help  
or you can have a look at manual which contains the output of all help commands

Usage: termicoder [OPTIONS] COMMAND [ARGS]...

  view, code & submit problems directly from terminal.

Commands:
  code    creates file with template code.  
  setup   sets up problem, contests and login.  
  submit  submit a solution.  
  test    test code against the sample testcases.  
  view    view contests, problems and problem statement
