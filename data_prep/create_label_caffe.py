from random import shuffle

train = []
test = []

for i in range(21798):
    if i < 4360:
        test.append("training/%06d.txt 1" % i)
    else:
        train.append("training/%06d.txt 1" % i)
for i in range(89664):
    if i < 17439:
        test.append("negatives/%06d.txt 0" % i)
    else:
        train.append("negatives/%06d.txt 0" % i)

shuffle(train)
shuffle(test)

test_file = open('test.txt', 'w')
train_file = open('train.txt', 'w')

for item in test:
    test_file.write("%s\n" % item)

for item in train:
    train_file.write("%s\n" % item)
