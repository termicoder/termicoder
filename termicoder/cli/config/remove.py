import click
import shutil
from ...utils.config import get_config_path, check_config_path
from ...utils.logging import logger


@click.command()
def main():
    """
    Remove the configuration directory.
    """

    if(check_config_path()):
        config_path = get_config_path()
        logger.warn("This will completely erase %s" % config_path)
        click.confirm("Continue?", abort=True)
        shutil.rmtree(config_path)
