import termicoder.utils.display as display
import click
import json
import subprocess
import os
import sys

browser_defaults_path = os.path.join(
    os.path.dirname(__file__), "browser_defaults.json")
browser_defaults_file = open(browser_defaults_path, "r")
browser_defaults = json.load(browser_defaults_file)


def view_contest(folder):
    contest_file_path = os.path.expanduser(folder)
    PORT = browser_defaults["port"]
    browser = browser_defaults["browser"]

    server_url = "http://localhost:" + PORT
    if(browser is None):
        click.launch(server_url)
        sys.exit()
    else:
        subprocess.call([browser, server_url])
    os.chdir(contest_file_path)
    try:
        subprocess.call(["python", "-m", "http.server", PORT])
    except Exception:
        click.echo("Unable to setup a server on localhost:" + PORT)


def edit_browser_defaults():
    click.confirm("This will open the json browser defaults file\n" +
                  "where you can edit default web browser\n"
                  "Do you want to conitnue?", default=True, abort=True)
    code_defaults_file = os.path.join(
        os.path.dirname(__file__),
        "browser_defaults.json")
    click.edit(filename=code_defaults_file)
    sys.exit()


def view_problem(folder):
    browser = browser_defaults["browser"]

    if(folder is None):
        problem_file_path = ".problem"
    else:
        problem_file_path = os.path.join(folder, ".problem")

    try:
        problem_file = open(problem_file_path, "r")
    except BaseException:
        display.file_read_error(problem_file_path, abort=True)

    problem = json.load(problem_file)

    if(folder is None):
        problem_html_path = problem["problem_code"]+".html"
    else:
        problem_html_path = os.path.join(
            folder, problem["problem_code"]+".html")

    if(browser is None):
        click.launch(problem_html_path)
        sys.exit()
    else:
        subprocess.call([browser, problem_html_path])


def view(folder, edit_defaults):
    if(edit_defaults):
        edit_browser_defaults()

    if(folder is None):
        problem_file_path = ".problem"
    else:
        problem_file_path = os.path.join(folder, ".problem")

    if(folder is None):
        contest_file_path = ".contest"
    else:
        contest_file_path = os.path.join(folder, ".contest")

    if (folder is None):
        folder = os.getcwd()

    if(".contest" in os.listdir(folder)):
        view_contest(folder)
    elif(".problem" in os.listdir(folder)):
        view_problem(folder)
    else:
        display.file_read_error(problem_file_path+"\n   or\n" +
                                contest_file_path, abort=True)
