# ViralOverlay™

Add styled, timed text to videos 'n GIFs!  Kinda like this:

![Beer](tester_shrunk_overlaid.gif)

# Usage

    vo [OPTIONS] FILEPATH OVERLAY_DATA

    OVERLAY_DATA: a JSON file path OR a JSON-formatted string containing an
    array of overlays, each containing key-value pairs of at least "text",
    "start", and "stop". optional keys: "font_size", "font_color",
    "text_position_x", and "text_position_y"

    Options:
      -g, --gif             output to GIF instead of MP4
      -f, --font-path TEXT  path to the font you'd like to use.
      --help                Show this message and exit.

## Example

    $ vo <path_to_video> <json_transcript_filepath_or_string> [--gif --font]

    (lots of ffmpeg output...)
    Okay, I overlaid your text on <path_to_video_overlaid>.

## JSON Transcript Format

The `json_transcript` string or file should look like this:

    [
        {
            "start": 1.03,
            "stop": 1.21,
            "text": "I"
        },
        {
            "start": 1.21,
            "stop": 1.44,
            "text": "am"
        },
        {
            "start": 1.45,
            "stop": 1.84,
            "text": "saying"
        },
        {
            "start": 1.85,
            "stop": 2.25,
            "text": "some"
        },
        {
            "start": 2.25,
            "stop": 2.97,
            "text": "words"
        }
    ]

See sibling projects [Transcribe all the Things](https://github.com/zevaverbach/tatt) and [tpro](https://github.com/zevaverbach/tpro) for easy, automatic generation of such transcripts.

# Installation

    pip install viraloverlay
    brew install ffmpeg  # (if you don't have ffmpeg already)
