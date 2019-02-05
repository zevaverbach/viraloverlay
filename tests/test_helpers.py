from unittest import mock

import pytest

from viraloverlay.exceptions import UnsupportedSystem
from helpers import (
        get_platform_font_path, 
        append_string_to_filepath
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
