import os
import json
import click
import termicoder.utils.display as display

supported_extensions = [".py", ".cpp", ".c", ".java", ".c++", ".cc"]


def get_judge():
    problem_file_path = ".problem"

    try:
        f = open(problem_file_path, "r")
    except BaseException:
        display.file_read_error(problem_file_path, abort=True)
    else:
        j = json.load(f)
        return j["judge"]


def get_file_name(file):
    # the file may be a str or a click.file return file name finally
    if(not isinstance(file, str)):
        return str(file.name)
    else:
        return str(file)

# this helps is reducing time as intelligently handling default


def get_code_file():
    probable_files = []
    for f in os.listdir(os.getcwd()):
        if(os.path.isfile(f) and os.path.splitext(f)[1] in supported_extensions):
            probable_files.append(f)

    default_file = None
    if(probable_files):
        default_file = probable_files[0]

    # defaulting to latest file
    for f in probable_files:
        if(os.path.getmtime(f) > os.path.getmtime(default_file)):
            default_file = f

    code_file = click.prompt('Please provide a code file', type=click.File(),
                             default=default_file)

    return code_file


def get_time_limit():
    time_limit = None
    problem_file_path = ".problem"

    try:
        f = open(problem_file_path, "r")
    except BaseException:
        pass
    else:
        j = json.load(f)
        try:
            time_limit = j["max_timelimit"]
        except BaseException:
            pass

    if(time_limit is None):
        return 3.0
    else:
        return float(time_limit)


def get_memory_limit():
    click.echo("memory_limit not implemented in this version")
