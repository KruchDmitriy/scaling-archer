import argparse
import os
from random import shuffle
  
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required = True, help = "path to KITTI dataset")

args = vars(parser.parse_args())
path = args["path"]  

print (path + "/prepared_data/training")
print (path + "/prepared_data/negatives")

pos_path = os.path.abspath(path + "/prepared_data/training") + "/"
neg_path = os.path.abspath(path + "/prepared_data/negatives") + "/"

pos_filenames = os.listdir(pos_path)
neg_filenames = os.listdir(neg_path)

pos_filenames = map((lambda x: pos_path + x + " 1"), pos_filenames)
neg_filenames = map((lambda x: neg_path + x + " 0"), neg_filenames)

pos_split = len(pos_filenames) / 5
neg_split = len(neg_filenames) / 5

train = pos_filenames[pos_split:]
test = pos_filenames[:pos_split]

train += neg_filenames[neg_split:]
test += neg_filenames[:neg_split]

shuffle(train)
shuffle(test)

test_file = open(path + "/prepared_data/test.txt", "w")
train_file = open(path + "/prepared_data/train.txt", "w")

for item in test:
    test_file.write("%s\n" % item)

for item in train:
    train_file.write("%s\n" % item)
