TCG Project #2
===

### Training
```python
# initial basic block
python3 ./threes.py --play="init save=output/weights.bin"

# keep training ( execute more time will be better )
python3 ./threes.py --total=100000 --block=1000 --limit=2000 --play="load=output/weights.bin save=output/weights.bin"
```

### Testing

```python
python3 ./threes.py --total=1000 --play="load=output/weights.bin" --save="output/stat.txt
```

Then you could send `output/stat.txt` to the judge.