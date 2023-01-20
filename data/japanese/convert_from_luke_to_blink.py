import argparse
import json
from typing import List, Optional, Union

from tqdm import tqdm
from wikipedia2vec.dump_db import DumpDB


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--luke-file", required=True)
    parser.add_argument("--output-file", required=True)
    parser.add_argument("--wikipedia-db", required=True)
    return parser.parse_args()


def make_blink_from_luke(luke_file: str, output_file: str, dump_db: DumpDB) -> None:
    def get_abstract(title: str) -> Optional[str]:
        try:
            abstract = "".join([paragraph.text for paragraph in dump_db.get_paragraphs(title) if paragraph.abstract])
        except KeyError:
            print (f"{title} is not included in db.")
            abstract = None

        return abstract

    label_counter = set()
    with open(luke_file) as i_f, open(output_file, "w") as o_f:
        for luke_sample in tqdm(i_f):
            luke_sample = json.loads(luke_sample.strip())
            mention_text = luke_sample["text"]
            selected_entities: List[List[Union[str, int]]] = luke_sample["selected_entities"]

            for entity in selected_entities:
                title, entity_id, start, end = entity
                abstract = get_abstract(title)
                if abstract is not None:

                    blink_sample = {
                        "mention": mention_text[start:end],
                        "context_left": mention_text[:start],
                        "context_right": mention_text[end:],
                        "label": abstract,
                        "label_title": title,
                        "label_id": entity_id,
                    }
                    o_f.write(json.dumps(blink_sample, ensure_ascii=False) + "\n")
                    label_counter.add(entity_id)

    print(f"total entity size: {len(label_counter)}")


def main():
    args = get_args()
    dump_db = DumpDB(args.wikipedia_db)
    make_blink_from_luke(args.luke_file, args.output_file, dump_db)


if __name__ == "__main__":
    main()
