import os
import argparse

import numpy
import matplotlib.pyplot as plt

from ffvideo import VideoStream

from make_page import make_page
from progress import progress


class VideoFrameGrabber(object):
    """Extracts frames at a fixed time step and saves them to a folder.

    Parameters
    ----------

    input_video_path : str
        Path to input video file.
    output_path : str
        Path to directory which will contain output frames as jpegs and html page.\
        Should be descriptive.
    frame_step : int
        Number of frames between samples.
    resize_factor : int
        Factor to resize frames by when saving.
    """
    def __init__(self, input_video_path, output_path, frame_step, resize_factor=2):
        self.input_video_path = input_video_path
        self.output_path = output_path
        self.frame_step = frame_step
        self.resize_factor = resize_factor

        self.vs = VideoStream(input_video_path)
        # self.duration = self.vs.duration
        self.total_frames = int(self.vs.duration * self.vs.framerate)

    def set_frame_step(self, frame_step):
        self.frame_step = frame_step

    def set_output_path(self, output_path):
        self.output_path = output_path

    def _make_output_directory(self):

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        frames_directory = os.path.join(self.output_path, 'static')
        if not os.path.exists(frames_directory):
            os.makedirs(frames_directory)

    def run(self, start_frame=0, end_frame=None):

        # Check input video exists.
        if not os.path.exists(self.input_video_path):
            raise Exception('Video does not exist!!')

        # Set up output directory.
        self._make_output_directory()

        # Save out frames to output directory.
        if not end_frame:
            end_frame = self.total_frames

        frames_to_get = numpy.arange(start_frame, end_frame, self.frame_step)
        frame_path_list = []

        prog = progress(len(frames_to_get))
        for i, frame in enumerate(frames_to_get):
            prog.update(i)
            video_frame = self.vs.get_frame_no(frame).image()
            width, height = video_frame.size
            new_size = (int(width/self.resize_factor), int(height/self.resize_factor))
            video_frame = video_frame.resize(new_size)
            filename = os.path.join(self.output_path, 'static', 'frame-%06d.jpeg' % frame)
            relative_path = os.path.join('static', 'frame-%06d.jpeg' % frame)
            video_frame.save(filename)
            frame_path_list.append(relative_path)

        frame_to_get_str_list = [str(frame) for frame in frames_to_get]
        prog.end()

        # Make webpage.
        make_page(self.output_path, 'index', frame_path_list, frame_to_get_str_list)


if __name__ == "__main__":

    # Parse Command Line Arguments
    parser = argparse.ArgumentParser(prog='frame_grabber', description='Script extract frames periodically from a video.')
    parser.add_argument('input_video_path', help='Path to video to be processed.')
    parser.add_argument('output_frames_path', help='Path to folder to save results.')
    parser.add_argument('--start_frame', default='0', help='First frame to sample.')
    parser.add_argument('--end_frame', default='None', help='Last frame to sample.')
    parser.add_argument('frame_step', help='Number of frames between samples.')
    args = parser.parse_args()

    # input_video_path = '/var/research/Databases/Face_Recog/Video_Face_UIUC/Inglourious_Basterds.mp4'
    # output_frames_path = '/home/pkhorra2/Desktop/Inglourious_Basterds_2'
    # time_step = 60
    input_video_path = args.input_video_path
    output_frames_path = args.output_frames_path
    start_frame = int(args.start_frame)
    if(args.end_frame == 'None'):
        end_frame = None
    else:
        end_frame = int(args.end_frame)
    frame_step = int(args.frame_step)

    frame_grabber = VideoFrameGrabber(input_video_path, output_frames_path, frame_step)
    frame_grabber.run(start_frame, end_frame)