TCG Project #2
===

### Training
```
# initial basic block
python3 ./threes.py --play="init save=output/weights.bin"

# keep training ( execute more time will be better )
python3 ./threes.py --total=100000 --block=1000 --limit=2000 --play="load=output/weights.bin save=output/weights.bin"
```

### Testing

```
python3 ./threes.py --total=1000 --play="load=output/weights.bin" --save="output/stat.txt
```

Then you could send `output/stat.txt` to the judge.


### Some Result ScreenShoot

| 6-tuples

<img width="75%" src="https://i.imgur.com/xyJe7jw.png">

| 4-tuples

<img width="75%" src="https://i.imgur.com/EKE6oqc.png">
