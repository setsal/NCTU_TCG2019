TCG Project #3
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


### 其他
有實作相關 bonus tile 的過程

如果需要我訓練之 weight.bin 可以聯繫我, e3 上不好放大檔案

隨圖附上一些 Judge 的成果

效果老實說不是太好QQ

![Imgur](https://i.imgur.com/mW5INMf.png)