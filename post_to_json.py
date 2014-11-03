import json

import numpy


def make_group(frame_numbers,
               data_array,
               group_id,
               frame_step=60,
               padding=30):
    clip_list = []

    group_frames = frame_numbers[numpy.where(data_array == group_id)]
    if len(group_frames) == 1:
        start_frame = group_frames[0] - padding
        end_frame = group_frames[0] + padding
        clip = (start_frame, end_frame)
        clip_list.append(clip)
    else:
        group_diffs = numpy.diff(group_frames/frame_step)

        start_frame = group_frames[0]
        count = 0
        for i, diff in enumerate(group_diffs):
            if diff == 1:
                count += 1
                end_frame = group_frames[i+1]
            if diff != 1 and count > 0:
                clip = (start_frame, end_frame)
                clip_list.append(clip)
                start_frame = group_frames[i+1]
                count = 0
            elif diff != 1 and count == 0:
                end_frame = start_frame + padding
                start_frame = start_frame - padding
                clip = (start_frame, end_frame)
                clip_list.append(clip)
                start_frame = group_frames[i+1]
        if count > 0:
            clip = (start_frame, end_frame)
            clip_list.append(clip)
        if count == 0:
            start_frame = group_frames[i+1]-padding
            end_frame = group_frames[i+1]+padding
            clip = (start_frame, end_frame)
            clip_list.append(clip)
    return clip_list

def post_to_json(data, frame_step=60):
    num_frames = len(data)

    frame_numbers = numpy.arange(0, num_frames*frame_step, frame_step)

    group_ids = numpy.unique(data)
    group_ids = group_ids[group_ids != ''] # remove empty strings
    sorted_index = numpy.argsort([int(group_id) for group_id in group_ids])
    group_ids = numpy.array(group_ids)[sorted_index]


    data_array = numpy.array(data)

    group_list = []
    for group_id in group_ids:
        print group_id
        group = make_group(frame_numbers, data_array, str(group_id))
        group_list.append(group)

    json.dump(group_list, open('clip.json', 'w'))