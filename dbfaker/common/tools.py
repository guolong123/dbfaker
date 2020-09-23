import os
import sys


def get_program_directory():
    app_dir = os.getcwd()
    if not app_dir:
        cmd = sys.argv[0]
        app_dir = None
        if cmd:
            app_dir, filename = os.path.split(cmd)

    return os.path.abspath(app_dir)


def check_path(path):
    if not os.path.isabs(path):
        path = os.path.join(get_program_directory(), path)
    return path


def get_current_path(current_path, path):
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.realpath(current_path)), path)
    return path
