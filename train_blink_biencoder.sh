export PYTHONPATH=.

BATCH=32
EPOCH=1
DATA=data/japanese/training
OUTPUT=models/debug

# lowercase は store_false
python blink/biencoder/train_biencoder.py \
  --output_path $OUTPUT \
  --bert_model cl-tohoku/bert-base-japanese-v2 \
  --lowercase \
  --train_batch_size $BATCH \
  --eval_batch_size 32 \
  --gradient_accumulation_steps 1 \
  --num_train_epochs $EPOCH \
  --data_path $DATA \
  --shuffle True \
  --eval_interval 100 \
  --debug 
