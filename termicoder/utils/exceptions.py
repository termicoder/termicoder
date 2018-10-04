import click
from .logging import logger
import sys


def handle_exceptions(*exceptions):
    """
    Used as a decorator.
    Takes exceptions and a function,
    returns function warpped with try except and debug functionality
    """
    # TODO correct the line number
    def wrapper(function):
        def customized_function(*args, **kwargs):
            logger.debug(
                "calling function %s" % sys.modules[function.__module__])
            try:
                function(*args, **kwargs)
            except (exceptions) as e:
                if(logger.level == 10):
                    raise
                else:
                    logger.error("in module %s:function %s:line %s" % (
                        sys.modules[function.__module__].__file__,
                        function.__name__, e.__traceback__.tb_lineno))
                    logger.error("%s %s" % (e.__class__.__name__, e))
                    raise click.Abort
        customized_function.__wrapped__ = True
        customized_function.__doc__ = function.__doc__
        return customized_function
    return wrapper
