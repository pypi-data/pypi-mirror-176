import sys
from . import colors

def join_args(f):
    def wrapper(*args, **kwargs):
        return f(' '.join(args), ', '.join('{}={}'.format(k, v) for k, v in kwargs.items()))
    return wrapper

@join_args
def success(message, details):
    if details:
        message = '{} ({})'.format(message, details)
    print(colors.GREEN + message + colors.DEFAULT)

@join_args
def warning(message, details):
    if details:
        message = '{} ({})'.format(message, details)
    print(colors.YELLOW + message + colors.DEFAULT)

@join_args
def failure(message, details):
    if details:
        message = '{} ({})'.format(message, details)
    print(colors.RED + message + colors.DEFAULT)

@join_args
def error(message, details):
    if details:
        message = '{} ({})'.format(message, details)
    raise SystemExit(colors.RED + message + colors.DEFAULT)

@join_args
def unknown_error(message):
    fcode = sys._getframe(1).f_code
    raise SystemExit(colors.RED + '{}:{} {}'.format(fcode.co_filename, fcode.co_name, message) + colors.DEFAULT)
