from .logging import logger
import os
from . import yaml
from .launch import launch, substitute


def folder(directory, browser_local):
    # TODO later migrate to flask based server
    logger.debug(os.listdir(directory))
    url = None
    if '.problem.yml' in os.listdir(directory):
        problem = yaml.read(os.path.join(directory, '.problem.yml'))
        url = os.path.join(directory, "%s.html" % problem.code)

    elif '.contest.yml' in os.listdir(directory):
        contest = yaml.read(os.path.join(directory, '.contest.yml'))
        logger.debug('launching contest %s' % contest.code)
        url = directory

    else:
        logger.error(".problem.yml and .contest.yml not found in folder")
        logger.error("Please make sure you are in correct directory")
        return
    keymap = {
       "FILE": url
    }
    status, browser_local = substitute(browser_local, keymap)
    if status is True:
        url = ''
    launch(browser_local, url)
