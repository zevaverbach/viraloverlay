"""
TODO: patch all tests to support any platform
(thinking particularly of the font_paths)
"""
import os
import tempfile
from unittest import mock

import pytest

import config
from viraloverlay.exceptions import UnsupportedSystem, NoOverlays
from helpers import UnsupportedSystem, append_string_to_filepath
from viraloverlay.viraloverlay import ViralOverlay


@pytest.fixture
def filepath():
    with tempfile.NamedTemporaryFile() as fp:
        yield fp.name


def test_that_nonexistent_filepath_raises_an_error():
    assert not os.path.exists('pretend_path.mp4')
    with pytest.raises(FileNotFoundError):
        viral_overlay = ViralOverlay('pretend_path.mp4')


@mock.patch('helpers.platform.system')
def test_that_font_selection_is_automatic_on_macos(patched_system, filepath):
    patched_system.return_value = 'Darwin'
    viral_overlay = ViralOverlay(filepath)
    assert viral_overlay.font_path == config.DARWIN_FONT_FILEPATH


@mock.patch('helpers.platform.system')
def test_that_font_selection_is_automatic_on_macos(patched_system, filepath):
    patched_system.return_value = 'Linux'
    with pytest.raises(UnsupportedSystem):
        viral_overlay = ViralOverlay(filepath)


def test_that_prepare_command_without_any_overlays_raises_an_error(filepath):
    viral_overlay = ViralOverlay(filepath)
    with pytest.raises(NoOverlays):
        viral_overlay._prepare_command()


def test_that_ffmpeg_command_is_as_expected_with_one_overlay(filepath):
    viral_overlay = ViralOverlay(filepath, overlays=('hi', 1, 2))
    viral_overlay._prepare_command()
    assert viral_overlay.command == (
        
       f"ffmpeg -y -i {filepath} -vf \"drawtext=enable='between(t,1,2)':"
       f"fontfile={config.DARWIN_FONT_FILEPATH}:text='hi':fontsize={config.FONT_SIZE}\""
        " -acodec copy "
       f"{append_string_to_filepath(filepath, config.APPEND_TO_OVERLAID_VIDS)}"
    )

def test_that_ffmpeg_command_is_as_expected_with_two_overlays(filepath):
    viral_overlay = ViralOverlay(
            filepath, 
            overlays=(('hi', 1, 2), ('bye', 5, 7))
            )
    viral_overlay._prepare_command()
    assert viral_overlay.command == (
        
       f"ffmpeg -y -i {filepath} -vf "
        "\"drawtext=enable='between(t,1,2)':"
        f"fontfile={config.DARWIN_FONT_FILEPATH}:text='hi':fontsize={config.FONT_SIZE},"
        "drawtext=enable='between(t,5,7)':"
        f"fontfile={config.DARWIN_FONT_FILEPATH}:text='bye':fontsize={config.FONT_SIZE}\""
        " -acodec copy "
       f"{append_string_to_filepath(filepath, config.APPEND_TO_OVERLAID_VIDS)}"
    )

def test_that_floats_work(filepath):
    viral_overlay = ViralOverlay(filepath, overlays=('hi', 1.5, 2.25))
    viral_overlay._prepare_command()
    assert viral_overlay.command == (
        
       f"ffmpeg -y -i {filepath} -vf \"drawtext=enable='between(t,1.5,2.25)':"
       f"fontfile={config.DARWIN_FONT_FILEPATH}:text='hi'\""
        " -acodec copy "
       f"{append_string_to_filepath(filepath, config.APPEND_TO_OVERLAID_VIDS)}"
    )



def test_that_it_works():
    test_file = os.getenv('VIRAL_OVERLAY_TEST_FILE')
    viral_overlay = ViralOverlay(test_file, overlays=('hi', 1, 2))
    viral_overlay.go()
    overlaid_file = append_string_to_filepath(test_file,
                                              config.APPEND_TO_OVERLAID_VIDS)
    assert os.path.exists(overlaid_file)
    os.remove(overlaid_file)
     
