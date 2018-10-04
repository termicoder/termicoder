import click
from ..utils.exceptions import handle_exceptions
from ..utils import config
from ..utils.logging import logger
from ..utils.launch import launch, substitute
from ..utils.load import get_default_code_name
import os


@click.command(short_help='Creates and opens file with template code.')
@click.argument('code_file',
                type=click.Path(writable=True, dir_okay=False),
                required=False)
@click.option('--editor',
              help="Specify the editor to launch the file with.",
              default=config.read('settings.yml', 'editor'))
@handle_exceptions(BaseException)
def main(code_file, editor):
    '''
    Creates and opens CODE_FILE with template code.

    If CODE_FILE already exists, 'code' just opens it in the default
    default/supplied editor without any change.

    If CODE_FILE is not passed, a default name of file is suggested
    based on current directory, language preferences and existing
    files in directory.

    Default CODE_FILE is <PROBLEM_NAME>.<DEFAULT_EXTENSION> if user is
    in a problem folder and no other supported code file exists.

    TODO [WIP]:
    If other code file(s) exist, it should suggests to open the most
    recently edited one.

    Template for the code is loaded based upon extension.

    See 'termicoder config' for editing default templates,
    editor, and language preferences.
    '''
    if code_file is None:
        default_name = get_default_code_name()
        code_file = click.prompt(
            "Please enter a file name", default=default_name,
            type=click.Path(writable=True, dir_okay=False))

    extension = code_file.split('.')[-1]
    template = config.read('lang/%s/template.yml' % extension)
    if(template is not None):
        try:
            code_to_write = template['code']
            # allow jinja style template substitution in command
            # example {{row_no}} and {{col_no}}
            # see settings.yml for info on usage
            status, editor = substitute(editor, template)
            # useful for sublime's go to line functionality
            # see settings.yml for info on usage
            status, editor = substitute(editor, {
                r"CODE_FILE": code_file
            })
            logger.debug(code_to_write)
        except (AttributeError, KeyError):
            logger.error("Probelm with template file")
    else:
        logger.warn("You don't have templates setup for extension %s."
                    "Launching empty file " % extension)
    if(not os.path.exists(code_file)):
        code = click.open_file(code_file, 'w')
        if(template is not None):
            code.write(code_to_write)
    if status:
        code_file = ''
    launch(editor, code_file)
