import math
import os
from subprocess import check_output
from typing import Union

from config import APPEND_TO_OVERLAID_VIDS, FONT_COLOR, FONT_SIZE
from helpers import (
        shell_call, 
        get_platform_font_path, 
        append_string_to_filepath
        )
from viraloverlay.exceptions import UnsupportedSystem, NoFont, NoOverlays

Numeric = Union[float, int]

class Overlay:

    def __init__(
            self, 
            text: str, 
            start: Numeric, 
            stop: Numeric, 
            font_path: str,
            font_size: int,
            font_color: int,
            ):
        self.text = text
        self.start = start
        self.stop = stop
        self.font_path = font_path
        self.font_size = font_size
        self.font_color = font_color

    def __str__(self):
        return (f"drawtext=enable='between(t,{self.start},{self.stop})':"
                f"fontfile={self.font_path}:fontcolor={self.font_color}:"
                f"text='{self.text}':fontsize={self.font_size}")


class ViralOverlay:

    # TODO: add colors, sizes, movement, position
    # https://ffmpeg.org/ffmpeg-filters.html#Examples-56

    def __init__(
            self, 
            filepath,
            font_path=None,
            font_color=None,
            font_size=None,
            overlays=None):
        """
        Each overlay should be a tuple in the format 
        (text, start, stop, <font_path>, <font_size>)

        """
        if font_path is None:
            try:
                font_path = get_platform_font_path()
            except UnsupportedSystem:
                raise UnsupportedSystem(
                        'Please provide a path to the font you\'d like to use')

        try:
            assert os.path.exists(filepath)
        except AssertionError:
            raise FileNotFoundError
        self.filepath = filepath
        validate_font_path(font_path)
        self.font_path = font_path
        self.font_size = font_size or FONT_SIZE
        self.font_color = font_color or FONT_COLOR
        self.overlays = []

        if overlays is not None:
            self.add(overlays)

    def go(self):
        self.export()

    def export(self):
        self._prepare_command()
        self._make()

    def _prepare_command(self):
        if not self.overlays:
            raise NoOverlays(
               'Please add at least one overlay tuple via `ViralOverlay.add`.')

        new_filepath = append_string_to_filepath(
                self.filepath,
                APPEND_TO_OVERLAID_VIDS)
        overlay_args = ','.join(str(o) for o in self.overlays)

        self.command = (
            f'ffmpeg -y -i {self.filepath} -vf "{overlay_args}" -acodec '
            f'copy {new_filepath}')

    def _make(self):
        return shell_call(self.command)

    def add(self, overlay_or_overlays):
        if not isinstance(overlay_or_overlays[0], tuple):
            overlays = [overlay_or_overlays]
        else:
            overlays = overlay_or_overlays

        for overlay in overlays:
            validate_overlay(overlay)
            if len(overlay) < 4:
                if self.font_path is None:
                    raise NoFont(
                        'Please provide a font_path either to ViralOverlay'
                        ' or each overlay')
                overlay = *overlay, self.font_path
            if len(overlay) < 5:
                if self.font_size is None:
                    raise NoFontSize(
                        'Please provide a font_size either to ViralOverlay'
                        ' or each overlay')
                overlay = *overlay, self.font_size
            if len(overlay) < 6:
                if self.font_color is None:
                    raise NoFontColor(
                       'Please provide a font_color either to ViralOverlay'
                       ' or each overlay')
                overlay = *overlay, self.font_color
            self.overlays.append(Overlay(*overlay))


def validate_overlay(overlay):
    if len(overlay) == 4:
        font_path = overlay[-1]
        assert isinstance(font_path, str)
        assert os.path.exists(font_path)
    text, start, stop = overlay[:3]
    assert isinstance(text, str)
    assert any(
            isinstance(start, type_) 
            for type_ in [int, float])
    assert any(
            isinstance(stop, type_)
            for type_ in [int, float])


def validate_font_path(font_path):
    assert os.path.exists(font_path)
    assert any(
            font_path.endswith(file_extension) 
            for file_extension in ['ttf', 'otf'])
