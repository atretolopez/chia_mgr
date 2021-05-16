
import os
import shutil

def is_tool(name):
    """Check whether `name` is on PATH."""
    from distutils.spawn import find_executable
    return find_executable(name) is not None

def getUserNamePath():
    '''
    Return current user name path
    :return: path to the current user
    '''
    if os.name == 'nt':
        return os.environ['USERPROFILE']
    elif os.name == 'posix':
        return "~"
    else:
        raise OSError("OS not supported")
