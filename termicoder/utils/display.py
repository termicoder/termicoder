import click
import sys
import termicoder.utils.style as style


def command(string):
    click.echo(style.command(string))


def error(string):
    click.echo(style.error(string))


def normal(string):
    click.echo(style.normal(string))


def print_url(string):
    click.echo(style.url(string))


def print_path(string):
    click.echo(style.path(string))


def url_error(url, abort):
    error("error in fetching url:")
    print_url(url)
    normal("please check your internet connection")
    if(abort):
        sys.exit()


def file_save_error(path, abort):
    error("error in saving file:")
    print_path(path)
    normal("please check the program has required permissions")
    if(abort):
        sys.exit()


def file_read_error(path, abort):
    error("error in reading file:")
    print_path(path)
    normal("please check that the file exists and\n" +
           "you are in correct directory/folder")
    if(abort):
        sys.exit()


def credential_error(judge, abort):
    error("error in logging into "+judge)
    normal("please check your credtials")
    if(abort):
        sys.exit()


def check_response_status(r, abort):
    try:
        r.raise_for_status()
    except BaseException:
        click.echo(style.error("error: the url ")+style.url(r.url))
        error("exited with status "+str(r.status_code))
        sys.exit()
