dir_count=0
for dir in ./ad-videos/*; do
	echo $dir
	for file in $dir/*; do
		echo $file
		ffmpeg -i $file -vf "select='eq(pict_type,PICT_TYPE_I)'" -keyint_min 1 -g 5 -q:v 5 -vsync 2 -f image2 caffe-singleframe-data/$((dir_count))_$(basename $file)_keyframe%04d.jpg -loglevel debug 2>&1 | grep pict_type:I | grep zz
		for image in caffe-singleframe-data/$((dir_count))_$(basename $file)_keyframe*.jpg; do
			echo $((dir_count))_$image $((dir_count)) >> caffe-singlefram-imagelist.txt
		done
	done
	dir_count=$((dir_count+1))
done