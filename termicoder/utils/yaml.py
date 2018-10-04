import click
import os
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from .logging import logger


def read(file_path, key=None, safe=False):
    if(not os.path.exists(file_path)):
        return None

    data_file = click.open_file(file_path)
    value = None
    try:
        data = yaml.load(data_file, Loader=Loader)
        data_file.close()
        logger.debug("read data from file %s" % file_path)
        logger.debug(data)
        logger.debug(key)
        if key is None:
            value = data
        else:
            value = data[key]
    except yaml.YAMLError as e:
        logger.error("yaml error" + str(e))
    except KeyError as e:
        logger.debug("KeyError key %s does not exist" % key)
    except TypeError as e:
        logger.debug("Type Error" + str(e))
    return value


def write(file_path, key, value):
    existing_data = read(file_path, None)
    if existing_data is None:
        existing_data = {}

    if key is not None:
        existing_data[key] = value
    else:
        existing_data = value
    data_file = click.open_file(file_path, 'w')
    try:
        logger.debug("writing data to file %s" % file_path)
        logger.debug(existing_data)
        yaml.dump(data=existing_data, stream=data_file, Dumper=Dumper)
    except yaml.YAMLError:
        raise
