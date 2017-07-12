import os
import json
import click
import termicoder.utils.display as display

supported_extensions=[".py",".cpp",".c",".java",".c++",".cc"]

def get_judge():
    problem_file_path=".problem"

    try:
        f=open(problem_file_path,"r")
    except:
        display.file_read_error(problem_file_path,abort=True)
    else:
        j=json.load(f)
        return j["judge"]

# this helps is reducing time as intelligently handling default
def get_code_file():
    probable_files=[]
    for f in os.listdir():
        if(os.path.isfile(f) and os.path.splitext(f)[1] in supported_extensions):
            probable_files.append(f)

    default_file=probable_files[0]

    # defaulting to latest file
    for f in probable_files:
        if(os.path.getmtime(f)>os.path.getmtime(default_file)):
            default_file=f

    code_file = click.prompt('Please provide a code file', type=click.File(),
    default=default_file)

    return default_file
