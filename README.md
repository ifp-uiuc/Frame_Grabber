# Frame_Grabber
This is a code repository to extract frames at periodic intervals from a video file.

First run:
``` shell
python frame_grabber.py --help
```

To get help. Then rerun `python frame_grabber.py` with the appropriate flags. Need to give it an `input_video_path`, `output_frames_path`, `frame_step`.

This will output:
+ directory of frame jpegs.
+ index.html

Next we will run the actual gui. Do this by running:

``` shell
python index.py
```

Use the gui, it will take a while to label a whole movie.

This will output:
+ clip.json

This is the most important file give it a more descriptive name, and keep it safe!!
