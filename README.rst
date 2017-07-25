Termicoder
==========

View, Code, Submit directly from terminal

Made with love by `Divesh Uttamchandani <https://github.com/diveshuttam/>`_

**Note: Termicoder is in its alpha stage and has only been tested on Ubuntu + python3 . Support for other configurations is being worked on, if you are using some other platform and encounter errors, do create a issue for them on** `github <https://github.com/diveshuttam/Termicoder/issues>`_


Installation
------------

User installation
~~~~~~~~~~~~~~~~~
Run the following commands in terminal/command prompt
    
    ::

	    pip install termicoder
	    use sudo -H if required. preferably use pip3 (python3)

Developer installation
~~~~~~~~~~~~~~~~~~~~~~
clone termicoder's repository
    
    ::

	    git clone https://github.com/diveshuttam/termicoder.git

in the root folder of repo run
    
    ::

        pip install --editable .
        notice the dot(.) in above command at the end
        Note: it is better to use virtualenv and pip3 (python3)

Autocomplete for bash
~~~~~~~~~~~~~~~~~~~~~

**Method 1**

    ::

        run the following command every time you use terminal
        eval "$(_TERMICODER_COMPLETE=source termicoder)"

**Method 2**

    ::

        put the following command in your .bashrc
        eval "$(_TERMICODER_COMPLETE=source termicoder)"

**Method 3**

    ::

 	    Method 2 makes bash to load up slowly, so try:
  	    eval "$(_TERMICODER_COMPLETE=source termicoder)" > autocomplete.sh
  	    and put . path_to_autocompte.sh/autocomplete.sh in your .bashrc

Current Support
---------------

Judges Supported Currently:
~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Iarcs Opc
2. CodeChef

Languages Supported Currently:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. C
2. C++
3. Java
4. Python2/3

Usage
-----
Only commands highlighted here,
for details we reccommend going through `sample run <https://github.com/diveshuttam/termicoder/blob/master/documentation/samplerun.md>`_ which contains detailed usage

for details of a particular command use

    ::

        termicoder --help
        termicoder <COMMAND> --help  
	
or you can have a look at `helptext <https://github.com/diveshuttam/termicoder/blob/master/documentation/helptext.md>`_ which contains the output of all help commands

    ::

        Usage: termicoder [OPTIONS] COMMAND [ARGS]...
        
	        view, code & submit problems directly from terminal.
	        
	    Commands:
	        code    creates file with template code.  
	        setup   sets up problem, contests and login.  
	        submit  submit a solution.  
	        test    test code against the sample testcases.  
	        view    view contests, problems and problem statement

Contribute
----------
Visit `Termicoder's homepage <https://github.com/diveshuttam/Termicoder>`_ for information on how to contribute

