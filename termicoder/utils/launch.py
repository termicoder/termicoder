import click
import subprocess
from .logging import logger


def launch(app_args, url):
    logger.debug(app_args)
    if(app_args is None):
        logger.warn('Preferred application is not set,'
                    'launching %s in default application' % url)
        click.launch(url)
    else:
        args = app_args[:]
        if(not isinstance(app_args, list)):
            args = [app_args]
        if(isinstance(args[0], list) and args[0] != []):
            launch(args[0], '')
            if(len(args) > 1):
                logger.debug("len>1")
                launch(args[1:], url)
            return
        logger.info('launching command with following params')
        logger.info(args)
        if url not in [None, '']:
            args.append(url)
        logger.debug(args)
        subprocess.run(args, check=True)


# returns (is_subsituted, args)
# substitute the markup strings ie {{..}}; in arguments
def substitute(args, keymap):
    logger.debug('in substitute args')
    logger.debug(args)
    logger.debug(keymap)
    if args not in [None, '', []]:
        if(not (isinstance(args, list))):
            logger.debug('executed base')
            final_args = args[:]
            for key in keymap:
                value = keymap[key]
                final_args = final_args.replace("{{%s}}" % key, str(value))
                logger.debug('final_args')
                logger.debug(final_args)
            status = final_args != args
        else:
            status1, temp_arg = substitute(args[0], keymap)
            status2, temp_arg1 = substitute(args[1:], keymap)
            if(temp_arg1 not in [None, '', []]):
                final_args = [temp_arg]
                final_args.extend(temp_arg1)
            else:
                final_args = [temp_arg]
            status = status1 or status2
            logger.debug('ran for')
            logger.debug(args[0])
            logger.debug(args[1:])
            logger.debug("got back")
            logger.debug(temp_arg)
            logger.debug(temp_arg1)

        logger.debug(keymap)
        logger.debug("args")
        logger.debug(final_args)
        return (status, final_args)
    else:
        return (False, None)
