srun -t "03:30:00"  -N 1 -p gpu -o "/home/kruchinin_d/Projects/scaling-archer/nn/caffenet_finetuned/test.txt" /home/kruchinin_d/lib/caffe/caffe/build/install/bin/caffe test -model "/home/kruchinin_d/Projects/scaling-archer/nn/caffenet_finetuned/test.prototxt" -weights "/home/kruchinin_d/Projects/scaling-archer/nn/caffenet_finetuned/caffenet_finetuned_iter_100000.caffemodel" -gpu 0 -iterations 78615 &
