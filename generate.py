import os
import json
import logging

from collections import defaultdict
from ourairports.parsers import parse_airports, parse_countries, parse_runways

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


def generate_countries():
    logging.info("loading and parsing countries")
    countries = parse_countries()
    logging.info("generating country list")
    country_list = [cntr.model_dump() for cntr in countries]
    logging.info("generating country map")
    country_map = {cntr.code: cntr.model_dump() for cntr in countries}
    logging.info("dumping country data")
    with open(f"{OUTPUT_FOLDER}/country_list.json", "w") as f:
        json.dump(country_list, f)
    with open(f"{OUTPUT_FOLDER}/country_map.json", "w") as f:
        json.dump(country_map, f)


def generate_runways():
    logging.info("loading and parsing runways")
    runways = parse_runways()
    logging.info("generating runway structures")
    runway_list = []
    runway_map = defaultdict(list)
    for rwy in runways:
        dump = rwy.model_dump()
        runway_list.append(dump)
        runway_map[rwy.airport_ident].append(dump)
    logging.info("dumping runway data")
    with open(f"{OUTPUT_FOLDER}/runway_list.json", "w") as f:
        json.dump(runway_list, f)
    with open(f"{OUTPUT_FOLDER}/runway_map.json", "w") as f:
        json.dump(runway_map, f)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    generate_airports()
    generate_countries()
    generate_runways()
