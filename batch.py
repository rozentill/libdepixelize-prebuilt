import os
from os.path import join
from argparse import ArgumentParser
import cv2
import numpy as np

def parse_args():
    
    parser = ArgumentParser()
    parser.add_argument('src_dir')
    parser.add_argument('dst_dir')

    args = parser.parse_args()
    return args.src_dir, args.dst_dir

def main():

	src_dir, dst_dir = parse_args()

	src_subdir = os.listdir(src_dir)

	for subdir in src_subdir:
		if not os.path.isdir(join(dst_dir, subdir)):
			os.mkdir(join(dst_dir, subdir))

		src_subfiles = os.listdir(join(src_dir, subdir))

		for subfile in src_subfiles:
			if not (subfile[-3:] == 'png' or subfile[-3:] == 'jpg'):
				continue
			#convert rgba to rgb
			im_rgba = cv2.imread(join(src_dir, subdir, subfile), cv2.IMREAD_UNCHANGED)

			im_rgba = im_rgba/255.
			if len(im_rgba.shape) == 2:
				im_rgba = np.expand_dims(im_rgba, axis=2)
				im_rgb = np.concatenate((im_rgba, im_rgba, im_rgba),axis=2)
			elif im_rgba.shape[2] == 4:
				im_rgb = im_rgba[:, :, :3]
				im_rgb[:, :, 0] = im_rgba[:,:, 0] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
				im_rgb[:, :, 1] = im_rgba[:,:, 1] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
				im_rgb[:, :, 2] = im_rgba[:,:, 2] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
			elif im_rgba.shape[2] == 3:
				im_rgb=im_rgba

			#padding
			h = im_rgb.shape[0]
			w = im_rgb.shape[1]
			c = im_rgb.shape[2]
			im_rgb_pad = np.ones((h+4, w+4, c))
			im_rgb_pad[2:h+2, 2:w+2, :] = im_rgb

			#output temp image
			tmp_file = "tmp.png"
			cv2.imwrite(tmp_file, im_rgb_pad*255)

			#call color trace
			trace_exe = "build/src/depixelize-kopf2011/depixelize-kopf2011"
			command_args = [trace_exe, "\"%s\""%tmp_file, "-o", "\"%s\""%join(dst_dir, subdir, subfile[:-4]+".svg"), "-c", "1", "-i", "5", "-m", "1", "-r", "4"]
			command_str = " ".join(command_args)
			os.system(command_str)


if __name__ == '__main__':
	
	main()
