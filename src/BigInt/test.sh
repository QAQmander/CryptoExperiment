#!/bin/bash

for((i=0;i<100;i++));
do
python3 gen.py
./a.out <input.txt >cout.txt
python3 test.py <input.txt >pyout.txt
cat input.txt
diff cout.txt pyout.txt
echo '\n'
done


