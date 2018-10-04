# for loading judge plugins
from pkg_resources import iter_entry_points
from . import Judge
from ..utils.Errors import JudgeNotFoundError
from ..utils import config
from ..utils.logging import logger
import sys


# Takes care of instantiating judges and keeping their session_data
# Decorates login logout methods of the judges to write session data
class JudgeFactory:
    def __init__(self):
        self.available_judges = []
        self._judge_classes = {}
        self._load_judges()

    def _load_judges(self):
        judges = iter_entry_points('termicoder.judge_plugins')
        for judge in judges:
            try:
                judge_class = judge.load()
                assert(issubclass(judge_class, Judge))
                # Try instantiating judge to check if abstract methods
                #  are implemented
                # TODO: see for a better alternative instead of instantiating
                self.available_judges.append(judge.name)
                judge_class()

                # decorate login and logout with _write_session_data
                judge_class.login = self._write_session_data(
                    judge.name)(judge_class.login)
                judge_class.logout = self._write_session_data(
                    judge.name)(judge_class.logout)

                self._judge_classes[judge.name] = judge_class

            # TODO log about 'why could not load judge'
            # also pass the exception instead of raising
            except AssertionError as e:
                logger.error("%s is not a subclass of Judge" % judge_class)
            except TypeError as e:
                # Abstract methods are not implemented
                logger.error(
                    "%s \ndoes not implement required "
                    "abstract methods of class Judge" % judge_class)
            except BaseException as e:
                logger.error(e)
                # think about something using click.abort without
                # printing traceback
                sys.exit(1)

        # sorting judges for statefulness
        self.available_judges.sort()

    def get_judge(self, judge_name):
        if(judge_name not in self.available_judges):
            raise JudgeNotFoundError
        else:
            # Return an instance of the judge
            # TODO load session data if available
            session_data = config.read('judges/sessions.yml', judge_name)
            return self._judge_classes[judge_name](session_data=session_data)

    def _write_session_data(self, judge_name):
        def decorator(function):
            def decorated_function(self_, *args, **kwargs):
                function(self_, *args, **kwargs)
                # TODO save to the appropriate location
                logger.debug("_write_session_data for %s" % judge_name)
                logger.debug(self_.session_data)
                config.write(
                    'judges/sessions.yml', judge_name, self_.session_data)
            return decorated_function
        return decorator
