import os
import cv2
import argparse
import re

# if the percent of area intersection < than this value, this is negative
ACCEPTED_PERCENT_INTERSECT = 0.3

def main()
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required = True, help = "path to Pascal VOC dataset (train)")
    parser.add_argument("-i", "--inter_perc", required = False,
        help = "if the percent of area intersection < than this value, this is negative")

    args = vars(parser.parse_args())

    if (args["inter_perc"] != ""):
        ACCEPTED_PERCENT_INTERSECT = float(args["inter_perc"])

    os.chdir(args["path"])

    img_names = open("ImageSets/Main/car_trainval.txt", "r")
    index = 0
    for name in img_names.readlines():
        name = name.split(" ")
        img = cv2.imread("JPEGImages/" + name[0] + ".jpg")
        if name[1] == "-1":
            #w, h = img.size()
            #side = (w / 5) if w >= h else (h / 5)
            #for i in range(h / side):
            #    for j in range(w / side):
            #        crop_img = img[i*side:(i+1)*side, j*side:(j+1)*side]
            #        dst = cv2.resize(crop_img, (227, 227))
            #        cv2.imwrite("prepared_data/%06d.jpg" % index, dst)
            #        index += 1
        else:
            annot = open("Annotations/" + name[0] + ".xml")

            pattern = r"\t\t<bndbox>\n.*<xmin>(?P<xmin>\d)<\\xmin>"
            #pattern = r"Iteration (?P<iter_num>\d+), loss = (?P<loss_val>\d+\.\d+e?[+-]?\d+)"
            result = parse_log(annot, pattern, 2)


            w, h = img.size()
            side = (w / 5) if w >= h else (h / 5)
            for i in range(h / side):
                for j in range(w / side):
                    crop_img = img[i*side:(i+1)*side, j*side:(j+1)*side]
                    dst = cv2.resize(crop_img, (227, 227))
                    cv2.imwrite("prepared_data/%06d.jpg" % index, dst)
                    index += 1

def parse_log(log_file, pattern, num_objects):
    with open(log_file, 'r') as log_file:
        log = log_file.read()

    objects = []
    for r in re.findall(pattern, log):
        str_tmp = ""
        if num_objects == 1:
            str_tmp = r
        else:
            for i in range(num_objects):
                str_tmp += r[i] + " "
            str_tmp += "\n"
        objects.append(str_tmp)
    return objects
