import os
os.environ["GLOG_minloglevel"] = "2"
import sys
import time
import shutil
import keyframes
import fileops
import path_params
import placesCNN
import tv_adnet

def main():

	overall_start = time.time()
	exec_time = time.strftime('%Y-%m-%d %H:%M')

	# Load model paths
	caffe_path = path_params.caffe_path
	pycaffe_path = path_params.pycaffe_path
	placesCNN_path = path_params.placesCNN_path
	tv_adnet_path = path_params.tv_adnet_path
	features_file = 'dummy.csv' #path_params.features_file

	# Start video processing
	clip_path = sys.argv[1]								## ../../dir/video.mp4
	rel_clip_path = clip_path.rsplit('/',1)[0] + '/'	## ../../dir/
	clip_name = clip_path.rsplit('/',1)[1]				## video.mp4
	clip = clip_name.rsplit('.',1)[0]					## video
	output_filename = clip 								## video
	clip_dir = rel_clip_path + clip + '/'				## ../../dir/video/

	# print rel_clip_path
	# print clip_name
	# print clip
	# print output_filename
	# print clip_dir

	if not os.path.exists(clip_dir):
		os.makedirs(clip_dir)
	else:
		shutil.rmtree(clip_dir)
		os.makedirs(clip_dir)
	shutil.copy(clip_path, clip_dir)
	new_clip_path = clip_dir + clip_name				## ../../dir/video/video.mp4

	keyframe_times = keyframes.keyframes(clip_dir, new_clip_path)
	keyframes_list = fileops.get_keyframeslist(clip_dir, new_clip_path)

	[all_images, all_timestamps] = fileops.rename_frames(clip_dir, keyframe_times, keyframes_list, [], [])

	if features_file == 'cropped_places_fc7.csv':
		image_files = cropframes.cropframes(clip_dir, all_images, new_clip_path)
		for image in all_images:
			os.remove(image)
	else:
		image_files = all_images
	
	os.remove(clip_dir + clip_name)

	print "Video preprocessing done...\n"

	# print keyframe_times
	# print keyframes_list

	# ## Run a model and get labels for keyframe
	# print "Running FC7 feature extraction from PlacesCNN...\n"
	# [fc7, scene_type_list, places_labels, scene_attributes_list] = placesCNN.placesCNN(pycaffe_path, placesCNN_path, image_files)
	# fileops.save_features(clip_dir + features_file, fc7)
	# print "Extracted fc7 features...\n"
	
	## Perform classification using the fine tuned ad model
	print "Running tv_adnet for category classification...\n"
	[tv_adnet_output, tv_adnet_labels] = tv_adnet.mynet(pycaffe_path, tv_adnet_path, image_files)
	print "(tv-adnet) Classified frames...\n"

	print "The top 5 [labels : probabilites] in order are:-"
	print tv_adnet_labels

	overall_end = time.time()	
	print "Total time taken: %.2f" %(overall_end-overall_start)

if __name__ == '__main__':
	main()