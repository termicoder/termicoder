import click
import os
import sys
import termicoder.utils.display as display
import termicoder.utils.parse as parse

lang_map={
".py":"python",
".c":"c",
".cpp":"cpp",
".cc":"cpp",
".c++":"cpp"
}

def get_script_type():
    if "nt" in os.name:
        return "bat"
    elif "posix" in os.name:
        return "bash"

def test(code_file):
    # code file will exist; thanks to 'click'
    display.normal("test not implemented yet")
    testcase_path=("testcase")
    time_limit = parse.get_time_limit()
    memory_limit = parse.get_memory_limit()
    # using customizable bash/bat scripts for test
    scripts_folder=os.path.join(os.path.dirname(__file__),"scripts")

    # if language is compiled
    # call scripts to compile ;then print time

    #call scripts to output to a file ; then print time
    #script takes arguments as in_filename and out_filename



def edit_scripts():
    click.confirm("This will open the scripts folder in file manager\n"+
    "Where you can edit compile and run scripts\n"
    "Do you want to contnue?",default=True,abort=True)
    scripts_folder=os.path.join(os.path.dirname(__file__),"scripts")
    click.launch(scripts_folder)
    sys.exit()
