import json
import math
import os
from pprint import pprint
import sys
from subprocess import check_output

from .config import (
        APPEND_TO_OVERLAID_VIDS,
        FONT_COLOR,
        FONT_SIZE,
        TEXT_POSITION_X,
        TEXT_POSITION_Y,
        MAX_ARG_CHARS,
        )
from .custom_types import Numeric
from .helpers import (
        shell_call, 
        get_platform_font_path, 
        append_string_to_filepath,
        )
from .exceptions import (
        UnsupportedSystem,
        NoFont,
        NoOverlays,
        MissingArgument,
        LengthError,
        )



class Overlay:

    def __init__(
            self, 
            text: str, 
            start: Numeric, 
            stop: Numeric, 
            font_path: str,
            font_size: int,
            font_color: int,
            text_position_x,
            text_position_y,
            ):
        self.text = text
        self.start = start
        self.stop = stop
        self.font_path = font_path
        self.font_size = font_size
        self.font_color = font_color

        self.text_position_x = text_position_x
        if isinstance(text_position_x, str):
            if text_position_x == 'center':
                self.text_position_x = 'x=(main_w/2-text_w/2)'

        self.text_position_y = text_position_y
        if isinstance(text_position_y, str):
            if text_position_y == 'bottom':
                self.text_position_y = 'y=main_h-(text_h*2)'

    def __str__(self):
        text = self.text.replace("'", "\\\\\\'")
        text = text.replace("[", "\\\\\[")
        text = text.replace("]", "\\\\\]")
        return (
                f"drawtext=enable='between(t,{self.start},{self.stop})':"
                f"fontfile={self.font_path}:"
                f"fontcolor={self.font_color}:"
                f'text="{text}":'
                f"fontsize={self.font_size}:"
                f"{self.text_position_x}:"
                f"{self.text_position_y}"
                )


class ViralOverlay:

    def __init__(
            self, 
            filepath,
            font_path=None,
            font_color=None,
            font_size=None,
            text_position_x=None,
            text_position_y=None,
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
        self.text_position_x = text_position_x or TEXT_POSITION_X
        self.text_position_y = text_position_y or TEXT_POSITION_Y
        self.overlays = []

        if overlays is not None:
            self.add(overlays)

    def go(self):
        return self.export()

    def gif(self):
        self._prepare_command(output_filetype='gif')
        return self._make()

    def export(self):
        self._prepare_command()
        return self._make()

    def _prepare_command(self, output_filetype=None):
        if not self.overlays:
            raise NoOverlays(
               'Please add at least one overlay tuple via `ViralOverlay.add`.')

        new_filepath = append_string_to_filepath(
                self.filepath,
                APPEND_TO_OVERLAID_VIDS)

        if output_filetype:
            new_filepath = '.'.join(new_filepath.split('.')[:-1]) + '.' + output_filetype
        overlay_arg_strings = []

        overlay_args = ','.join(str(o) for o in self.overlays)

        if len(overlay_args) > MAX_ARG_CHARS:
            raise LengthError(
                f'Your system only allows {MAX_ARG_CHARS} characters in a command,'
                f' and the one generated here is {len(overlay_args)}!')

        self.command = (
            f'ffmpeg -y -i {self.filepath} -vf "{overlay_args}" -acodec '
            f'copy {new_filepath}')

        self.new_filepath = new_filepath

    def _make(self):
        shell_call(self.command)
        return self.new_filepath

    def add(self, overlay_or_overlays):
        if isinstance(overlay_or_overlays, tuple):
            overlays = overlay_or_overlays
        elif isinstance(overlay_or_overlays, list):
            overlays = tuple(overlay_or_overlays)
        else:
            if isinstance(overlay_or_overlays, str):
                overlays_path = overlay_or_overlays
                with open(overlays_path) as fin:
                    overlays = json.load(fin)
            else:
                overlays = [overlay_or_overlays]

        for overlay in overlays:
            overlay = self.validate_and_fortify_overlay(overlay)
            self.overlays.append(Overlay(**overlay))

    def validate_and_fortify_overlay(self, overlay):
        if any(key not in overlay for key in ['text', 'start', 'stop']):
            pprint(overlay)
            raise MissingArgument

        overlay['font_path'] = overlay.get('font_path') or self.font_path
        overlay['font_size'] = overlay.get('font_size') or self.font_size
        overlay['font_color'] = overlay.get('font_color') or self.font_color
        overlay['text_position_x'] = (overlay.get('text_position_x')
                                      or self.text_position_x)
        overlay['text_position_y'] = (overlay.get('text_position_y')
                                      or self.text_position_y)

        return overlay


def validate_font_path(font_path):
    assert os.path.exists(font_path)
    assert any(
            font_path.endswith(file_extension) 
            for file_extension in ['ttf', 'otf'])
