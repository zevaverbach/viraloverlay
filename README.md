# ViralOverlay™

Add styled, timed text to videos 'n GIFs!  Kinda like this:

![Beer](tester_shrunk_overlaid.gif)

# Usage

    $ vo <path_to_video> <path_to_json_transcript OR json_transcript_string> [--gif if you want a gif instead of an mp4]

    (lots of ffmpeg output...)
    Okay, I overlaid your text on <path_to_video_overlaid>.

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
