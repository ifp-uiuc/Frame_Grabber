import os
import argparse
import json

from frame_grabber import VideoFrameGrabber


if __name__ == "__main__":
    
    # Parse Command Line Arguments
    parser = argparse.ArgumentParser(prog='clip_grabber', description='Script extract frames periodically from a video.')
    parser.add_argument('input_video_path', help='Path to video to be processed.')
    parser.add_argument('output_frames_path', help='Path to folder to save results.')
    parser.add_argument('json_file', help='Text that specifies individual video clips.')
    parser.add_argument('frame_step', help='Number of frames between samples.')
    parser.add_argument('--padding', default='0', help='Additional frames to grab at start and end of clip.')
    args = parser.parse_args()

    input_video_path = args.input_video_path
    output_frames_path = args.output_frames_path
    json_file = args.json_file
    frame_step = int(args.frame_step)
    padding = int(args.padding)

    # Create VideoFrameGrabber object to parse each tuple in tuples_text_file
    frame_grabber = VideoFrameGrabber(input_video_path, output_frames_path, frame_step)

    # Read in clips from .json file
    clip_list = json.load(open(json_file, 'rb'))
    print clip_list
    print 'Number of groups: %d' % len(clip_list)

    # Create folders for each group.
    for i, group in enumerate(clip_list):
        print 'Number of clips in group %d: %d' % (i, len(group))
        group_name = 'group_%04d' % i
        group_path = os.path.join(output_frames_path, group_name)
        if not os.path.exists(group_path):
            os.makedirs(group_path)

        # Create subfolder for each clip.
        for j, clip in enumerate(group):
            clip_name = 'clip_%02d' % j
            clip_path = os.path.join(group_path, clip_name)

            if not os.path.exists(clip_path):
                os.makedirs(clip_path)

            # Call frame grabber on clip.
            frame_grabber.set_output_path(clip_path)
            frame_grabber.run(clip[0]-padding, clip[1]+padding)



