import numpy as np
import re
import argparse
from os import system, remove


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required = True, help = "path to log")

    args = vars(parser.parse_args())
    file = args["file"]

    pattern = r"Iteration (?P<iter_num>\d+), loss = (?P<loss_val>\d+\.\d+e?[+-]?\d+)"
    result = parse_log(file, pattern, 2)
    train = open("train.txt", "w")
    for str_tmp in result:
        train.write(str_tmp)

    pattern = r"Iteration (?P<iter_num>\d+), Testing net \(#0\)\n.*\n.*\n.*\n.*\n.* Test net output #4: loss3/loss3 = (?P<loss3>\d+\.\d+e?[+-]?\d+).*\n.* Test net output #5: loss3/top-1 = (?P<accuracy>\d+\.\d+e?[+-]?\d+)"
    result = parse_log(file, pattern, 3)
    test = open("test.txt", "w")
    for str_tmp in result:
        test.write(str_tmp)


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

def plot(result_file, name):
    tmp = open("tmp.gp", "w")
    text = "set terminal png truecolor size 350, 300\n\
            set output '" + name + ".png'\n\
            set ylabel \"minutes\" font ", 20"\n\
            set yrange [0:70]\n\
            set title \"" + name + "\" font \", 20\"\
            plot '" + result_file + "' using 1:2 with lines"

if __name__ == '__main__':
    main()
