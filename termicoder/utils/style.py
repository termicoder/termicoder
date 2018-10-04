import click


def _style_decorator(fg, bg=None, underline=None, bold=None):
    def decorated_function(*args, **kwargs):
        return click.style(*args, **kwargs, fg=fg,
                           bg=bg, bold=bold, underline=underline)
    return decorated_function


# TODO add option for changing colors from config file
error = _style_decorator('red')
message = _style_decorator('white')
url = _style_decorator('cyan', underline=True)
ac = _style_decorator('green')
partial_ac = _style_decorator('yellow')
wrong = _style_decorator('red')
headers = _style_decorator('blue')

__all__ = ['error', 'message', 'url', 'ac', 'partial_ac', 'wrong', 'headers']
