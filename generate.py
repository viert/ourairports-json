import os
import json
import logging
import sys

from ourairports.parsers import parse_airports
from ourairports.misc import repo_changed

OUTPUT_FOLDER = "output"


def generate_airports():
    logging.info("loading and parsing airports")
    airports = parse_airports()
    logging.info("generating airport list")
    arpt_list = [arpt.model_dump() for arpt in airports]
    logging.info("generating airport map")
    arpt_map = {arpt.ident: arpt.model_dump() for arpt in airports}
    logging.info("dumping airport data")
    with open(f"{OUTPUT_FOLDER}/airport_list.json", "w") as f:
        json.dump(arpt_list, f)
    with open(f"{OUTPUT_FOLDER}/airport_map.json", "w") as f:
        json.dump(arpt_map, f)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    generate_airports()
    if repo_changed():
        sys.exit(1)
    sys.exit(0)
