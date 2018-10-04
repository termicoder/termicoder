import click
from ...utils.config import get_config_path


@click.command()
def main():
    """
    Edit the configuration.

    Launches the config folder for modifying settings.
    """

    config_path = get_config_path(ensure_exists=True)
    click.launch(config_path)
