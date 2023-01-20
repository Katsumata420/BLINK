# How to prepare BLINK training data

## 1. Prepare envs

```bash
$ pwd
>> /path/to/BLINK
$ pip install -r requirements.txt
```

## 2. Make Luke pretraining data
Blink pretraining data can be derived from Luke pretraining data.

Please see [this Luke's README.md](https://github.com/Katsumata420/luke/blob/pretraining-dataset-jsonl/README-PRETRAIN-DATA.md).

## 3. Make Blink pretraining data from Luke data

```bash
$ pwd
>> /path/to/BLINK/data/japanese
$ python convert_from_luke_to_blink.py \
  --luke-file /path/to/Luke-data.jsonl \
  --wikipedia-db /path/to/jawiki.db \  # This db would be created when creating Luke data.
  --output-file /path/to/Blink-data.jsonl
```

Blink data format is following:

```json
{
    "mention": "",
    "context_left": "",
    "context_right": "",
    "label": "",
    "label_title": "",
    "label_id": 0
}
```

### Note
- If you want to sample the above data, use `sampling_data.py`.
  - The sampling size is coding in this script.

```bash
$ wc /path/to/Blink-data.jsonl
>> xx line
$ python sampling_data.py \
  --original-jsonl /path/to/Blink-data.jsonl \
  --original-line-size xx \
  --output-dir /path/to/sampled-output
```

Then, training and validation data is created in `/path/to/sampled-output`.
