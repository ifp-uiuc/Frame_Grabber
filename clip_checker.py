from jinja2 import Environment, PackageLoader

def ls_filtered(path, filter_string):
    contents = os.listdir(path)
    filtered_list = sorted([content for content in contents if content.startswith(filter_string)])
    filtered_array = numpy.array(filtered_list)
    return filtered_array

path = 'clips_out/'

env = Environment(loader=PackageLoader('frame_grabber', 'templates'))
template = env.get_template('clip_checker.html')

group_dirs = ls_filtered(path, 'group')

groups = []
for group_dir in group_dirs:
    group = dict()
    clips = []

    group_path = os.path.join(path, group_dir)
    clip_data = ls_filtered(group_path, 'clip')

    if len(clip_data) % 2 != 0:
        raise Exception('Missing clip data.')

    num_clips = len(clip_data)/2

    for i in range(num_clips):
        clip = dict()
        clip['name'] = 'clip_%02d' % i
        clip['pairwise_mse'] = os.path.join(group_path, 'clip_%02d_pairwise_mse.jpeg' % i)
        clip['mean'] = os.path.join(group_path, 'clip_%02d_mean.jpeg' % i)
        clips.append(clip)

    group['name'] = group_dir
    group['mean'] = os.path.join(group_path, 'group_mean.jpeg')
    group['clips'] = clips
    groups.append(group)

html = template.render(groups=groups)

f = open('out.html', 'w')
f.write(html)
f.close()