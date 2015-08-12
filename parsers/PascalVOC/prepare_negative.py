import os
import cv2
import argparse
import re

def main():
    # if the percent of area intersection < than this value, this is negative
    ACCEPTED_PERCENT_INTERSECT = 0.3

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required = True, help = "path to Pascal VOC dataset (train)")
    parser.add_argument("-i", "--inter_perc", required = False,
        help = "if the percent of area intersection < than this value, this is negative")

    args = vars(parser.parse_args())

    if (args["inter_perc"] != ""):
        ACCEPTED_PERCENT_INTERSECT = float(args["inter_perc"])
    print ACCEPTED_PERCENT_INTERSECT

    os.chdir(args["path"])

    img_names = open("ImageSets/Main/car_trainval.txt", "r")
    index = 0
    for name in img_names.readlines():
        name = name.split(" ")
        img = cv2.imread("JPEGImages/" + name[0] + ".jpg")
        if name[1] == "-1\n":
            h, w, c = img.shape
            side = (w / 5) if w >= h else (h / 5)
            for i in range(h / side):
                for j in range(w / side):
                    crop_img = img[i*side:(i+1)*side, j*side:(j+1)*side]
                    dst = cv2.resize(crop_img, (227, 227))
                    cv2.imwrite("prepared_data/%06d.jpg" % index, dst)
                    index += 1
        else:
            annot = "Annotations/" + name[0] + ".xml"
            pattern = r"\t\t<bndbox>\n.*<xmin>(?P<xmin>\d+)</xmin>\n.*<ymin>(?P<ymin>\d+)</ymin>\n.*<xmax>(?P<xmax>\d+)</xmax>\n.*<ymax>(?P<ymax>\d+)</ymax>"
            bboxs = parse_log(annot, pattern, 4)
            print annot
	    
            h, w, c = img.shape
            side = (w / 5) if w >= h else (h / 5)
            for i in range(h / side):
                for j in range(w / side):
            	    accept = True
            	    for bbox in bboxs:
                	# left, top, right, bottom
	        	# compute area intersection
    	        	left = min(max(bbox[0], j*side), (j+1)*side)
    	        	top = min(max(bbox[1], i*side), (i+1)*side)
    	        	right = max(min(bbox[2], (j+1)*side), j*side)
    	        	bottom = max(min(bbox[3], (i+1)*side), i*side)
    	        	percent_inter = float((bottom - top) * (right - left)) / float((side * side))
            		if (percent_inter > ACCEPTED_PERCENT_INTERSECT):
            		    accept = False
            	    if accept:
                	crop_img = img[i*side:(i+1)*side, j*side:(j+1)*side]
                	dst = cv2.resize(crop_img, (227, 227))
                	cv2.imwrite("prepared_data/%06d.jpg" % index, dst)
                	index += 1
            print index

def parse_log(log_file, pattern, num_objects):
    with open(log_file, 'r') as log_file:
        log = log_file.read()

    objects = []
    for r in re.findall(pattern, log):
        tmp = []
        if num_objects == 1:
            tmp = int(r)
        else:
            for i in range(num_objects):
                tmp.append(int(r[i]))
        objects.append(tmp)
    return objects

if __name__ == '__main__':
    main()