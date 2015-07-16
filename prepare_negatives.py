import os
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required = True, help = "path to KITTI dataset")
args = vars(parser.parse_args())

os.chdir(args["path"])

index = 0
for i in range(0, 7480):
	image = cv2.imread("training/image_2/%06d.png" % i)
	label = open("training/label_2/%06d.txt" % i)
	content = label.readlines()
	bboxs = []
	for line in content:
		words = line.split(" ")
		if (
			words[0] == "Car" or words[0] == "Van" or words[0] == "Truck"
			):
			bbox = map(int, map(float, words[4:8]))
			# left, top, right, bottom
			bboxs = bboxs + bbox
			#crop_img = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
			#
			#dst = cv2.resize(crop_img, (227, 227))
			#cv2.imwrite("prepared_data/%06d.png" % index, dst)
	# i -> [0, 374] first: 0, second 374 - 227 = 47
	# j -> [0, 1241] 1: 0, 2: 227, ..., 6: 1241 - 227 = 1014
	for j in range(1, 6):
		# if and so on

	index += 1
	print(index)