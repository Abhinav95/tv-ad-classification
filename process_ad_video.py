import os
import sys
import time
os.environ["GLOG_minloglevel"] = "2"
import keyframes
import fileops
import shutil

def main():

	overall_start = time.time()
	exec_time = time.strftime('%Y-%m-%d %H:%M')

	features_file = '.'

	# Start video processing
	clip_path = sys.argv[1]								## ../../dir/video.mp4
	rel_clip_path = clip_path.rsplit('/',1)[0] + '/'	## ../../dir/
	clip_name = clip_path.rsplit('/',1)[1]				## video.mp4
	clip = clip_name.rsplit('.',1)[0]					## video
	output_filename = clip 								## video
	clip_dir = rel_clip_path + clip + '/'				## ../../dir/video/

	print rel_clip_path
	print clip_name
	print clip
	print output_filename
	print clip_dir

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

	print keyframe_times
	print keyframes_list

	overall_end = time.time()	
	print "Total time taken: %.2f" %(overall_end-overall_start)

if __name__ == '__main__':
	main()