import os
import platform
from subprocess import check_output

import config
from viraloverlay.exceptions import UnsupportedSystem


def shell_call(command):
    return check_output(command, shell=True)


def get_platform_font_path():
    system = platform.system()
    if system != 'Darwin':
        raise UnsupportedSystem
    return config.DARWIN_FONT_FILEPATH


def append_string_to_filepath(filepath, string):
    basename, extension = os.path.splitext(filepath)
    return f'{basename}{string}{extension}'
