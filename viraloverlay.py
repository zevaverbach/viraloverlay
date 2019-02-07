import sys
from viraloverlay.viraloverlay import ViralOverlay



if __name__ == '__main__':
    args = sys.argv
    v = ViralOverlay(args[1], overlays=args[2])
    if len(args) > 3 and args[3] == 'gif':
        v.gif()
    else:
        v.go()
