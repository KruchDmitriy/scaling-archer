import os
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required = True, help = "path to KITTI dataset")
parser.add_argument("-i", "--inter_perc", required = False, type=float, default=0.3,
        help = "if the percent of area intersection < than this value, this is negative")

args = vars(parser.parse_args())
ACCEPTED_PERCENT_INTERSECT = args["inter_perc"]

os.chdir(args["path"])
os.mkdir("prepared_data/negatives")

# hardcore
# (i_min, i_max, j_min, j_max)
# (left, top, right, bottom)
# i -> [0, 374] first: 0, second 374 - 227 = 47
# j -> [0, 1241] 1: 0, 2: 227, ..., 6: 1241 - 227 = 1014

area = [
        [(0,   0, 227,  227),  (227,  0, 454,  227),
         (454, 0, 681,  227),  (681,  0, 908,  227),
         (908, 0, 1135, 227),  (1015, 0, 1242, 227)],
        [(0,   148, 227,  375), (227,  148, 454,  375),
         (454, 148, 681,  375), (681,  148, 908,  375),
         (908, 148, 1135, 375), (1015, 148, 1242, 375)]
]


index = 0
for num_file in range(0, 7481):
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
            bboxs[len(bboxs):] = [bbox]
    for i in range(0, 2):
        for j in range(0, 6):
            cur_area = area[i][j]
            accept = True
            for bbox in bboxs:
                # left, top, right, bottom
                # compute area intersection
                # print(bbox)
                # print(cur_area)
                left = max(bbox[0], cur_area[0])
                top = max(bbox[1], cur_area[1])
                right = min(bbox[2], cur_area[2])
                bottom = min(bbox[3], cur_area[3])
                percent_inter = (bottom - top) * (right - left) / (227 * 227)
                if (percent_inter > ACCEPTED_PERCENT_INTERSECT):
                    accept = False
            if accept:
                dst = image[cur_area[1]:cur_area[3], cur_area[0]:cur_area[2]]
                if (len(dst) != 227 or len(dst[0]) != 227):
                    dst = cv2.resize(dst, (227, 227))
                cv2.imwrite("prepared_data/negatives/%06d.png" % index, dst)
                index += 1
                print(index)
