import argparse
import os
import random

from tqdm import tqdm


TRAIN_SIZE = 9_000_000
VALID_SIZE = 1_000_000

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--original-jsonl", required=True, help="original blink train data")
    parser.add_argument("--original-line-size", required=True, type=int, help="line size in original train data.")
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def sample_data(original_file: str, output_dir: str, train_ratio: float, valid_ratio: float, margin_ratio: float) -> None:
    train_file = os.path.join(output_dir, "train.jsonl")
    valid_file = os.path.join(output_dir, "valid.jsonl")

    counter = {"train": 0, "valid": 0}
    with open(original_file) as i_f, open(train_file, "w") as t_f, open(valid_file, "w") as v_f:
        for line in tqdm(i_f):
            if counter["train"] >= TRAIN_SIZE and counter["valid"] >= VALID_SIZE:
                print("Fin.")
                break
            line = line.strip()
            prob = random.uniform(0, 1)
            if prob < train_ratio + margin_ratio:
                t_f.write(line + "\n")
                counter["train"] += 1
            elif train_ratio + margin_ratio <= prob < train_ratio + valid_ratio + 2 * margin_ratio:
                v_f.write(line + "\n")
                counter["valid"] += 1


def main():
    args = get_args()
    
    train_ratio = TRAIN_SIZE / args.original_line_size
    valid_ratio = VALID_SIZE / args.original_line_size
    margin_ratio = 0.05
    print(f"train size: {TRAIN_SIZE}; ratio: {train_ratio}")
    print(f"valid size: {VALID_SIZE}; ratio: {valid_ratio}")

    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    sample_data(args.original_jsonl, args.output_dir, train_ratio, valid_ratio, margin_ratio)
    

if __name__ == "__main__":
    main()
