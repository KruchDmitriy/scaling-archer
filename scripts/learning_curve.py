import numpy as np
import re
import argparse
import subprocess
from os import remove


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required = True, help = "path to log")
    parser.add_argument("-o", "--output", required = True, help = "path to plots")

    args = vars(parser.parse_args())
    file = args["file"]

    pattern = r"Iteration (?P<iter_num>\d+), loss = (?P<loss_val>\d+\.\d+e?[+-]?\d+)"
    result = parse_log(file, pattern, 2)
    train = open("train.txt", "w")
    for str_tmp in result:
        train.write(str_tmp)
    train.close()
    
    pattern = r"Iteration (?P<iter_num>\d+), Testing net \(#0\)\n.*\n.*\n.*\n.*\n.* Test net output #4: loss3/loss3 = (?P<loss3>\d+\.\d+e?[+-]?\d+).*\n.* Test net output #5: loss3/top-1 = (?P<accuracy>\d+\.\d+e?[+-]?\d+)"
    result = parse_log(file, pattern, 3)
    test = open("test.txt", "w")
    for str_tmp in result:
        test.write(str_tmp)
    test.close()

    out = args["output"]
    plot("train.txt", "1:2", out, "train", "loss", True)
    plot("test.txt", "1:2", out, "test", "loss", True)
    plot("test.txt", "1:3", out, "test_acc", "accuracy", False)

    remove("train.txt")
    remove("test.txt")


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

def plot(result_file, columns, path, name, ylabel, logscale):
    tmp = open("tmp.gp", "w")
    sharp_ls = ""
    if not logscale:
	sharp_ls += "#"
    text = "set terminal png truecolor size 1024, 512\n\
            set output '" + path + "/" + name + ".png'\n\
            " + sharp_ls + "set logscale y\n\
            set xlabel 'iterations'\n\
            set ylabel '" + ylabel + "' \n\
            set title '" + name + "' \n\
            plot '" + result_file + "' using " + columns + " with lines smooth bezier\n"
    tmp.write(text)
    tmp.close()
    subprocess.call(["gnuplot", "tmp.gp"])
    remove('tmp.gp')

if __name__ == '__main__':
    main()
