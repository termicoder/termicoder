import click
import sys
import os
import termicoder.utils.style as style

def command(string):
    click.echo(style.command(string))

def error(string):
    click.echo(style.error(string))

def normal(string):
    click.echo(style.normal(string))

def print_url(string):
    click.echo(style.url(string))

def current_dir(cwd):
    click.echo("current working directory is: %s" % cwd)
    click.echo("display directory not implemented yet")

def url_error(url,abort):
    error("error in fetching:")
    print_url(url)
    normal("please check your internet connection")
    if(abort):
        sys.exit()
