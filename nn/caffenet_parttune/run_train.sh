srun -t "24:00:00" -o "/home/kruchinin_d/Projects/scaling-archer/nn/caffenet_parttune/log.txt" -N 1 -p gpu /home/kruchinin_d/lib/caffe/build/tools/caffe train -solver /home/kruchinin_d/Projects/scaling-archer/nn/caffenet_parttune/solver.prototxt -weights /home/kruchinin_d/Projects/scaling-archer/nn/caffenet/bvlc_reference_caffenet.caffemodel &
