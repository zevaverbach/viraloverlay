import json
import math
import os
from subprocess import check_output

from config import APPEND_TO_OVERLAID_VIDS, FONT_COLOR, FONT_SIZE
from custom_types import Numeric
from helpers import (
        shell_call, 
        get_platform_font_path, 
        append_string_to_filepath
        )
from viraloverlay.exceptions import (
        UnsupportedSystem,
        NoFont,
        NoOverlays,
        MissingArgument,
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
            ):
        self.text = text
        self.start = start
        self.stop = stop
        self.font_path = font_path
        self.font_size = font_size
        self.font_color = font_color

    def __str__(self):
        return (
                f"drawtext=enable='between(t,{self.start},{self.stop})':"
                f"fontfile={self.font_path}:"
                f"fontcolor={self.font_color}:"
                f"text='{self.text}':"
                f"fontsize={self.font_size}"
                )


class ViralOverlay:

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
        if not isinstance(overlay_or_overlays, tuple):
            if isinstance(overlay_or_overlays, str):
                overlays_path = overlay_or_overlays
                with open(overlays_path) as fin:
                    overlays = json.load(fin)
            else:
                overlays = [overlay_or_overlays]
        else:
            overlays = overlay_or_overlays

        for overlay in overlays:
            overlay = self.validate_and_fortify_overlay(overlay)
            self.overlays.append(Overlay(**overlay))

    def validate_and_fortify_overlay(self, overlay):
        if (not overlay.get('text')
                or not overlay.get('start')
                or not overlay.get('stop')
                ):
            raise MissingArgument

        overlay['font_path'] = overlay.get('font_path') or self.font_path
        overlay['font_size'] = overlay.get('font_size') or self.font_size
        overlay['font_color'] = overlay.get('font_color') or self.font_color

        return overlay


def validate_font_path(font_path):
    assert os.path.exists(font_path)
    assert any(
            font_path.endswith(file_extension) 
            for file_extension in ['ttf', 'otf'])
