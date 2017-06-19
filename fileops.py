import os,sys
import numpy as np
import csv, re

def get_keyframeslist(clip_dir, clip_path):

	clip = clip_path.split('/')[-1]
	clip_name = clip.split('.')[0]
	
	keyframes_list = []
	source = sorted(os.listdir(clip_dir))

	for file in source:
		if file.endswith(".jpg") and file.startswith(clip_name + '_keyframe'):
			image = clip_dir + os.path.basename(file)
			keyframes_list.append(image)

	return keyframes_list

def atoi(text):
    return int(text) if text.isdigit() else text
def natural_sorting(item):
	return [atoi(c) for c in re.split('(\d+)', item)]

def get_pyframeslist(clip_dir, clip_name):

	pyframes_list = []
	source = sorted(os.listdir(clip_dir))
	
	for file in source:
		if file.endswith("IN.jpg") or file.endswith('OUT.jpg'):
			image = clip_dir + os.path.basename(file)
			pyframes_list.append(image)

	pyframes_list.sort(key = natural_sorting)		

	return pyframes_list

def rename_frames(clip_dir, timestamps, keyframes, extra_timestamps, pyframes):

	for timestamp, keyframe in zip(timestamps, keyframes):
		timestamp = "{0:.3f}".format(float(timestamp))
		os.rename(keyframe, clip_dir + timestamp + '.jpg')

	for extra_timestamp, pyframe in zip(extra_timestamps, pyframes):
		extra_timestamp = "{0:.3f}".format(float(extra_timestamp))
		os.rename(pyframe, clip_dir + extra_timestamp + '.jpg')

	image_files = []
	new_times = []
	source = sorted(os.listdir(clip_dir))
	
	for file in source:
		if file.endswith(".jpg"):
			image = clip_dir + os.path.basename(file)
			image_files.append(image)

			fname = os.path.basename(file)
			fname = fname.rsplit('.',1)[0]
			fname = float(fname)
			new_times.append(fname)
			
	new_times.sort()
	image_files.sort(key = natural_sorting)

	return image_files, new_times

def save_features(filename, features):
	np.savetxt(filename, features, fmt = '%.6f', delimiter=',')

def get_video_filename(clip_dir):

	source = os.listdir(clip_dir)
	mp4_flag = 0

	for file in source:
		if file.endswith(".mp4"):
			if mp4_flag == 0:
				clip_name = os.path.basename(file)
				mp4_flag = 1
			else:
				print "Multiple mp4 files! Quitting..."
				exit(0)

	return clip_name

def get_cropped(clip_dir):

	source = sorted(os.listdir(clip_dir))
	images = []
	for file in source:
		if file.endswith('.jpg'):
			images.append(clip_dir + file)

	return images