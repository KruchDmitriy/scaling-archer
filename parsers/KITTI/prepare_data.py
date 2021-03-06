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
    for line in content:
        words = line.split(" ")
        if (
            (words[0] == "Car" or words[0] == "Van" or words [0] == "Truck") and
            (float(words[1]) < 0.5) and (int(words[2]) < 2)
            ):
            bbox = map(int, map(float, words[4:8]))
            # left, top, right, bottom
            # make surounding
            bbox[0] -= 16
            bbox[0] = 0 if bbox[0] < 0 else bbox[0]
            bbox[1] -= 16
            bbox[1] = 0 if bbox[1] < 0 else bbox[1]
            bbox[2] += 16
            bbox[2] = 1241 if bbox[2] >= 1241 else bbox[2]
            bbox[3] += 16
            bbox[3] = 374 if bbox[3] >= 374 else bbox[3]

            crop_img = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]

            dst = cv2.resize(crop_img, (227, 227))
            cv2.imwrite("prepared_data/training/%06d.png" % index, dst)
            index += 1
            print(index)
