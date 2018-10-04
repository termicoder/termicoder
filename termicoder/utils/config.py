import click
import os
from builtins import FileNotFoundError
from .import yaml as localYAML
from .logging import logger


def get_config_path(ensure_exists=False):
    config_path = click.get_app_dir('termicoder')
    if(ensure_exists is True and not os.path.exists(config_path)):
        logger.error(
            "Termicoder config not initialized\n"
            "Requested operation requires configuration files to proceed\n"
            "Run `termicoder config init` and try executing this command again"
        )
        raise click.Abort("Config not initialized")
    return config_path


def check_config_path():
    config_path = get_config_path()
    return os.path.exists(config_path)


# TODO handle exceptions and messages in a better way
# TODO `load` and `safe_load` properly.
# In places, it may be more powerful to use load instead of safe_load
# (yaml files can call funcions if using load)

# rel_path is relative to the config_path
# currently safe=True is not supported yet
# key = None return the whole config
def read(rel_path, key=None, safe=False):
    if(safe is True):
        # use safe load later
        pass

    data_path = os.path.join(get_config_path(), rel_path)
    value = localYAML.read(data_path, key, safe)
    return value


# if key is none, rewrite the whole file with value
def write(rel_path, key, value):
    data_path = os.path.join(get_config_path(), rel_path)
    if(os.path.exists(data_path) is False):
        raise FileNotFoundError
    value = localYAML.write(data_path, key, value)
