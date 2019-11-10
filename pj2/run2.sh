#!/bin/sh
python3 ./threes.py --total=10000 --block=1000 --limit=2000 --play="load=output/weights.bin" --save="output/stat.txt"
