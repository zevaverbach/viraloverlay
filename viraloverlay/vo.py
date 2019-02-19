import json
from pathlib import Path

import click

from .viraloverlay import ViralOverlay


@click.command()
@click.option('-g', '--gif', is_flag=True, help='output to GIF instead of MP4')
@click.argument('filepath', type=click.Path(exists=True))
@click.argument('overlay_data', type=str)
def cli(filepath, overlay_data, gif):
    """
    Creates a new video with text overlaid on it.

       overlay_data: a JSON file path
                     OR
                     a JSON-formatted string containing an array of overlays, 
                     each containing key-value pairs of at least 
                         "text", "start", and "stop".
                     optional keys: "font_size", "font_color", "text_position_x", 
                         and "text_position_y"
    """
    if overlay_data.endswith('.json') and Path(overlay_data).exists():
        with open(overlay_data) as fin:
            overlay_data_json = json.loads(fin.read())
    else:
        overlay_data_json = tuple(json.loads(overlay_data))
    v = ViralOverlay(filepath, overlays=overlay_data_json)
    method = v.gif if gif else v.go
    new_filepath = method()
    print(f'Okay, I overlaid your text on {new_filepath}')
