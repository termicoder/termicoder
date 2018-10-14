import click
from ....utils.exceptions import handle_exceptions
from ....utils.logging import logger
import sys
import subprocess
import os
import shutil
from builtins import PermissionError

@click.command()
@handle_exceptions(BaseException)
def main():
    """
    Setup man pages.
    """
    if sys.platform == "linux":
        try:
            usr_page_dir = '/usr/local/share/man/man1/'
            logger.info('')
            manpage_dir = os.path.join(os.path.dirname(__file__), 'pages')
            for manpage in os.listdir(manpage_dir):
                manpage_src = os.path.join(manpage_dir, manpage)
                manpage_dst = os.path.join(usr_page_dir, manpage)
                shutil.copy2(manpage_src, manpage_dst)
            subprocess.call(['mandb'])
        except PermissionError:
            logger.error("Permission denied! Try running with sudo!")
    else:
        logger.error('Manpages install for the platform is not supported yet')


__all__ = ['main']
