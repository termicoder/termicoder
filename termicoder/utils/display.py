import click


def display(text, nl=True,  stderr=False):
    click.echo(message=text, nl=nl, err=stderr)
