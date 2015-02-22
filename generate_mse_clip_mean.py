import os

import Image
import numpy
from matplotlib import pyplot

def ls_jpegs(path):
    contents = os.listdir(path)
    jpeg_list = sorted([content for content in contents if content.endswith('.jpeg')])
    jpeg_array = numpy.array(jpeg_list)
    return jpeg_array

def ls_filtered(path, filter_string):
    contents = os.listdir(path)
    filtered_list = sorted([content for content in contents if content.startswith(filter_string)])
    filtered_array = numpy.array(filtered_list)
    return filtered_array

def find_anchor_indices(jpeg_array, frame_step=60):
    jpeg_list = list(jpeg_array)
    frame_index_list = [int(jpeg.split('-')[1].split('.')[0]) for jpeg in jpeg_list]
    is_anchor = (numpy.array(frame_index_list) % frame_step) == 0
    anchor_indices = numpy.where(is_anchor)[0]
    return anchor_indices

def calculate_pairwise_mse(path, jpeg_array):
    mse_list_pairwise = []

    for i in range(len(jpeg_array)-1):
        cur_jpeg_path = os.path.join(path, jpeg_array[i])
        cur_frame = numpy.array(Image.open(cur_jpeg_path))
        next_jpeg_path = os.path.join(path, jpeg_array[i+1])
        next_frame = numpy.array(Image.open(next_jpeg_path))
        mse = numpy.mean((cur_frame - next_frame)**2)
        mse_list_pairwise.append(mse)
    return mse_list_pairwise

def plot_results(anchor_indices, pairwise_mse, passed_segments, path, title, threshold=50, save=True):
    for segment in passed_segments:
        pyplot.axvspan(segment[0], segment[1], facecolor='g', alpha=0.2)
    
    pyplot.plot(pairwise_mse)

    for anchor in anchor_indices:
        pyplot.plot([anchor, anchor],[0, 100], 'g')

    # Theshold annotation
    pyplot.plot([0, len(pairwise_mse)], [threshold, threshold], 'r')
    pyplot.title(title)
    pyplot.xlabel('relative frame number')
    pyplot.ylabel('mse')
    
    if save:
        filename = os.path.join(path, title)
        pyplot.savefig(filename)
        pyplot.show()
    
def filter_clip(pairwise_mse, anchor_indices, threshold=50):
    endpoints = numpy.array(pairwise_mse) > threshold
    endpoints[0] = 1
    endpoints[-1] = 1
    bins = numpy.where(endpoints)[0]
    counts = numpy.histogram(anchor_indices, bins=bins)[0]
    segments_to_pass = numpy.where(counts>0)[0]
    segments_to_filter = numpy.where(counts==0)[0]
    passed_segments = []
    filtered_segments = []
    for segment in segments_to_pass:
        segment_start = bins[segment]
        segment_end = bins[segment+1]
        passed_segment = (segment_start, segment_end)
        passed_segments.append(passed_segment)
    for segment in segments_to_filter:
        segment_start = bins[segment]
        segment_end = bins[segment+1]
        filtered_segment = (segment_start, segment_end)
        filtered_segments.append(filtered_segment)
    return passed_segments, filtered_segments

def calculate_mean_segment(path, jpeg_array, segments):
    image_size = numpy.array(Image.open(os.path.join(path, jpeg_array[0]))).shape
    mean_array = numpy.zeros(image_size, dtype=numpy.float32)
    count = 1
    for segment in segments:
        for i in range(segment[0], segment[1]):
            jpeg = jpeg_array[i]
            temp_image = numpy.array(Image.open(os.path.join(path, jpeg)))
            mean_array = mean_array + (temp_image - mean_array)/count
            count += 1
    return mean_array

def update_group_mean_segment(clip_mean, count, group_mean=None):
    if group_mean is None:
        image_size = clip_mean.shape
        group_mean = numpy.zeros(image_size, dtype=numpy.float32)
    
    group_mean = group_mean + (clip_mean - group_mean)/(count+1)
    return group_mean

path = './Casino_Royal/clips/'
out_path = './Casino_Royal/clips_out/'
threshold = 70

group_array = ls_filtered(path, 'group')

for i_group, group in enumerate(group_array):
    group_path = os.path.join(path, group)
    group_out_path = os.path.join(out_path, 'group_%04d' % i_group)
    if not os.path.exists(group_out_path):
        os.makedirs(group_out_path)
    
    clip_array = ls_filtered(group_path, 'clip')
    for i_clip, clip in enumerate(clip_array):
        clip_path = os.path.join(path, group, clip, 'static')
        jpeg_array = ls_jpegs(clip_path)
        anchor_indices = find_anchor_indices(jpeg_array)
        pairwise_mse = calculate_pairwise_mse(clip_path, jpeg_array)
        passed_segments, filtered_segments = filter_clip(pairwise_mse, anchor_indices, threshold=threshold)
        
        plot_results(anchor_indices, pairwise_mse, passed_segments, group_out_path, title='clip_%02d_pairwise_mse.jpeg' % (i_clip), threshold=threshold)
        clip_mean = calculate_mean_segment(clip_path, jpeg_array, passed_segments)
        clip_mean_image = Image.fromarray(numpy.uint8(clip_mean))
        filename = os.path.join(group_out_path, 'clip_%02d_mean.jpeg' % (i_clip))
        print 'saving clip mean to %s.' % filename
        clip_mean_image.save(filename)
        if i_clip == 0:
            group_mean = update_group_mean_segment(clip_mean, i_clip)
        else:
            group_mean = update_group_mean_segment(clip_mean, i_clip, group_mean=group_mean)
    group_mean_image = Image.fromarray(numpy.uint8(group_mean))
    filename = os.path.join(group_out_path, 'group_mean.jpeg')
    print 'saving group mean to %s.' % filename
    group_mean_image.save(filename)
    #pyplot.imshow(numpy.uint8(clip_mean))
    #pyplot.show()