import subprocess

DARWIN_FONT_FILEPATH = '/Library/Fonts/Microsoft/Arial.ttf'
APPEND_TO_OVERLAID_VIDS = '_overlaid'
FONT_SIZE = 90
FONT_COLOR = 'white'
TEXT_POSITION_X = 'center'
TEXT_POSITION_Y = 'bottom'
MAX_ARG_CHARS = int(subprocess.check_output('getconf ARG_MAX', shell=True).decode().strip())
