import argparse
from random import shuffle
  
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required = True, help = "path to KITTI dataset")

args = vars(parser.parse_args())
path = args["path"]  

train = []
test = []

for i in range(21798):
    if i < 4360:
        test.append(path + ("/prepared_data/training/%06d.png 1" % i))
    else:
        train.append(path + ("/prepared_data/training/%06d.png 1" % i))
for i in range(89664):
    if i < 17439:
        test.append(path + ("/prepared_data/negatives/%06d.png 0" % i))
    else:
        train.append(path + ("/prepared_data/negatives/%06d.png 0" % i))

shuffle(train)
shuffle(test)

test_file = open(path + '/prepared_data/test.txt', 'w')
train_file = open(path + '/prepared_data/train.txt', 'w')

for item in test:
    test_file.write("%s\n" % item)

for item in train:
    train_file.write("%s\n" % item)
