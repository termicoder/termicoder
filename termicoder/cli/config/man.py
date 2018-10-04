import click
from ...utils.exceptions import handle_exceptions


@click.command()
@handle_exceptions(BaseException)
def main():
    """
    Setup man pages.
    """
    raise NotImplementedError("Not implemented in this version")
