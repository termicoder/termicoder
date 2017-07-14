import click
import os
import sys
import termicoder.utils.display as display
import termicoder.utils.parse as parse

def edit_templates():
    click.confirm("This will open the templates folder in file manager\n"+
    "Where you can edit templates for various languages\n"
    "Do you want to conitnue?",default=True,abort=True)
    templates_folder=os.path.join(os.path.dirname(__file__),"templates")
    click.launch(templates_folder)
    sys.exit()

def edit_defaults():
    click.confirm("This will open the json code default file\n"+
    "where you can edit default editors for various languages\n"
    "Do you want to conitnue?",default=True,abort=True)
    code_defaults_file=os.path.join(os.path.dirname(__file__),"code_defaults.json")
    click.launch(code_defaults_file)
    sys.exit()
