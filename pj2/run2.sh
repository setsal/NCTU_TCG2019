#!/bin/sh
python3 ./threes.py --total=100000 --block=1000 --limit=1000 --play="load=output/weights.bin" --save="output/stat.txt"
