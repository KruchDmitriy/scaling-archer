import os
import cv2
import argparse

# if the percent of area intersection < than this value, this is negative
ACCEPTED_PERCENT_INTERSECT = 0.3

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required = True, help = "path to KITTI dataset")
parser.add_argument("-i", "--inter_perc", required = False,
	help = "if the percent of area intersection < than this value, this is negative")

args = vars(parser.parse_args())

if (args["inter_perc"] != ""):
	ACCEPTED_PERCENT_INTERSECT = float(args["inter_perc"])

os.chdir(args["path"])

# hardcore
# (i_min, i_max, j_min, j_max)
# (left, top, right, bottom)
# i -> [0, 374] first: 0, second 374 - 227 = 47
# j -> [0, 1241] 1: 0, 2: 227, ..., 6: 1241 - 227 = 1014

area = [
	[(0,   0, 226,  226),  (227,  0, 453,  226),
	 (454, 0, 680,  226),  (681,  0, 907,  226),
	 (908, 0, 1134, 226),  (1014, 0, 1241, 226)],
	[(0,   47, 226,  374), (227,  47, 453,  374),
	 (454, 47, 680,  374), (681,  47, 907,  374),
	 (908, 47, 1134, 374), (1014, 47, 1241, 374)]
]


index = 0
for num_file in range(0, 7480):
	image = cv2.imread("training/image_2/%06d.png" % num_file)
	label = open("training/label_2/%06d.txt" % num_file)
	content = label.readlines()
	bboxs = []
	for line in content:
		words = line.split(" ")
		if (
			words[0] == "Car" or words[0] == "Van" or words[0] == "Truck"
			):
			bbox = map(int, map(float, words[4:8]))
			bboxs = bboxs + bbox
	for i in range(0, 2):
		for j in range(0, 6):
			accept = true
			for bbox in bboxs:
				# left, top, right, bottom
				# compute area intersection
				left = max(bbox[0], area[0])
				top = max(bbox[1], area[1])
				right = min(bbox[2], area[2])
				bottom = min(bbox[3], area[3])
				percent_inter = (bottom - top) * (right - left) / (227 * 227)
				if (percent_inter > ACCEPTED_PERCENT_INTERSECT):
					accept = false
			if accept:
				crop_img = image[area[1]:area[3], area[0]:area[2]]
				cv2.imwrite("prepared_data/negatives/%06d.png" % index, dst)
				index += 1
				print(index)

