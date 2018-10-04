from .import config
from . import yaml
import os


# TODO check if other recently modified code files are present
# if yes then return the most recent one as the default file
def get_default_code_name():
    default_name = config.read('settings.yml', 'default_code_file')
    if ".problem.yml" in os.listdir():
        problem = yaml.read('.problem.yml')
        default_name = problem.code + "." + config.read(
            'settings.yml', 'default_extension')
    return default_name


def get_problem_or_contest(folder):
    if ".contest.yml" in os.listdir(folder):
        return yaml.read(os.path.join(folder, '.contest.yml'))
    elif ".problem.yml" in os.listdir(folder):
        return yaml.read(os.path.join(folder, '.problem.yml'))
