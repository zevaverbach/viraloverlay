import os
import platform
import re
from subprocess import check_output

from . import config
from .custom_types import Numeric
from .exceptions import UnsupportedSystem


def shell_call(command):
    return check_output(command, shell=True)


def get_platform_font_path():
    system = platform.system()
    if system == 'Darwin':
        return config.DARWIN_FONT_FILEPATH
    elif system == 'Linux':
        return get_linux_font_filepath()
    else:
        raise UnsupportedSystem


def get_all_font_paths():
    raw_font_list = subprocess.check_output(
            'fc-list', shell=True).decode().split('\n')
    font_paths = [f.split(':')[0] for f in raw_font_list]


def get_linux_font_filepath():
    all_font_paths = get_all_font_paths()
    for font_path in all_font_paths:
        if 'LiberationSans-Regular.ttf' in font_path:
            return font_path
    return all_font_paths[0]


def append_string_to_filepath(filepath, string):
    basename, extension = os.path.splitext(filepath)
    return f'{basename}{string}{extension}'


def get_excerpt(filepath, start, duration, outpath=None):
    if not outpath:
        basename, extension = os.path.splitext(filepath)
    outpath = outpath or make_excerpt_filename(filepath, start, duration)
    start_hhmmss, duration_hhmmss = num_to_hhmmss(start), num_to_hhmmss(duration)
    return check_output(
            _make_excerpt_command(
                filepath, 
                start_hhmmss,
                duration_hhmmss,
                outpath)
        )


def _make_excerpt_command(filepath, start_hhmmss, duration_hhmmss, outpath):
    return (f'ffmpeg -i {filepath} -ss {start_hhmmss} '
            f'-t {duration_hhmmss} -async 1 {outpath}')


def make_excerpt_filename(filepath, start, duration):
    return append_string_to_filepath(
        filepath,
        f'''
_{str(start).replace(".", "_")}_to_{str((start + duration)).replace(".", "_")}
         '''.strip()
        )


def num_to_hhmmss(num: Numeric):
    decaseconds = ''
    seconds = f"{num % 60:0>2}"
    if '.' in seconds:
        seconds, decaseconds = seconds.split('.')
        decaseconds = f'.{decaseconds}'
        decaseconds = f'{float(decaseconds):.1f}'.replace('0.', '.')
        if decaseconds.count('.') > 1:
            decaseconds = ''.join(decaseconds.split('.')[:-1])
        seconds = f'{seconds:0>2}'
    minutes = f"{int(num) // 60 % 60:0>2}"
    hours = f"{int(num) // 3600:0>2}"
    hhmmss = f"{hours}:{minutes}:{seconds}{decaseconds}"
    return hhmmss


def shrink_video(filepath):
    new_filepath = f'{os.path.splitext(filepath)[0]}_shrunk.mp4'
    shell_call(f'ffmpeg -i "{filepath}" -vf scale=480:260 "{new_filepath}"')
    return new_filepath

