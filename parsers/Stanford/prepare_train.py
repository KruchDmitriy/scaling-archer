import os
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required = True, help = "path to Stanford dataset")
args = vars(parser.parse_args())

os.chdir(args["path"])

label = open("train_annos_2.txt")
label.readline()

for l in label.readlines():
    # img, left, top, right, bottom
    image = cv2.imread("cars_train/" + l[0])
    print(l[0])
    crop_img = image[l[2]:l[4], l[1]:l[3]]
    dst = cv2.resize(crop_img, (227, 227))
    cv2.imwrite("prepared_data/train/" + l[0], dst)
