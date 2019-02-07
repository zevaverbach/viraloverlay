from unittest import mock

import pytest

from viraloverlay.exceptions import UnsupportedSystem
from helpers import (
        get_platform_font_path, 
        append_string_to_filepath,
        make_excerpt_filename,
        _make_excerpt_command,
        num_to_hhmmss,
        )



@mock.patch('platform.system')
def test_get_platform_font_path(patched_system):

    patched_system.return_value = 'Darwin'
    assert get_platform_font_path() == \
            '/Library/Fonts/Microsoft/Arial.ttf'

    patched_system.return_value = 'Linux'
    with pytest.raises(UnsupportedSystem):
        get_platform_font_path()

    patched_system.return_value = 'Windows'
    with pytest.raises(UnsupportedSystem):
        get_platform_font_path()


def test_append_string_to_filepath():
    assert append_string_to_filepath('hi.txt', '_there') == 'hi_there.txt'


def test_make_excerpt_filename():
    assert make_excerpt_filename('hi.mp4', 2.5, 5) == 'hi_2_5_to_7_5.mp4'


def test_make_excerpt_command():
    assert _make_excerpt_command(
            'hi.mp4', 
            '00:00:02.5',
            '00:00:07.5',
            'out.mp4'
            ) == (f'ffmpeg -i hi.mp4 -ss 00:00:02.5 '
                  f'-t 00:00:07.5 -async 1 out.mp4'
    )


def test_num_to_hhmmss():
    assert num_to_hhmmss(2.5) == '00:00:02.5'
    assert num_to_hhmmss(4) == '00:00:04'
    assert num_to_hhmmss(120) == '00:02:00'
