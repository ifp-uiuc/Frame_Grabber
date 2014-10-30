import os

import Image
import numpy

def compute_group_mean(group_path):

    clip_list = sorted(os.listdir(group_path))
    clip_path = os.path.join(group_path, clip_list[0], 'frames')
    frame_list = sorted(os.listdir(clip_path))

    image_size = numpy.array(Image.open(os.path.join(clip_path, frame_list[0]))).shape
    mean_array = numpy.zeros(image_size, dtype=numpy.float32)

    count = 1
    for i, clip in enumerate(clip_list):
        clip_path = os.path.join(group_path, clip, 'frames')
        frame_list = sorted(os.listdir(clip_path))
        for j, frame in enumerate(frame_list):
            temp_image = numpy.array(Image.open(os.path.join(clip_path, frame)))
            mean_array = mean_array + (temp_image - mean_array)/count
            count += 1

    mean_image = Image.fromarray(numpy.uint8(mean_array))
    mean_image.save('mean.jpeg')
    