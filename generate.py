import os
import json
import logging

from collections import defaultdict
from ourairports.parsers import parse_airports, parse_countries, parse_runways, parse_navaids, parse_regions, parse_frequencies
from ourairports.types import AirportExtended

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

    logging.info("loading and parsing frequencies")
    freqs = parse_frequencies()

    logging.info("generating extended airport structures")
    arpt_list = []
    arpt_map = {}

    for arpt in airports:
        freq_list = freqs.get(arpt.id)
        arpt = AirportExtended(**arpt.model_dump())
        if freq_list is not None:
            freq_map = defaultdict(list)
            for freq in freq_list:
                freq_map[freq.type].append(freq.to_ext())
            arpt.frequencies = dict(freq_map)
        arpt_list.append(arpt.model_dump())
        arpt_map[arpt.ident] = arpt.model_dump()

    with open(f"{OUTPUT_FOLDER}/airport_ext_list.json", "w") as f:
        json.dump(arpt_list, f)
    with open(f"{OUTPUT_FOLDER}/airport_ext_map.json", "w") as f:
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
    runway_split_map = defaultdict(dict)
    for rwy in runways:
        dump = rwy.model_dump()
        runway_list.append(dump)
        runway_map[rwy.airport_ident].append(dump)
        rwy1, rwy2 = [r.model_dump() for r in rwy.split()]
        runway_split_map[rwy.airport_ident][rwy1["ident"]] = rwy1
        runway_split_map[rwy.airport_ident][rwy2["ident"]] = rwy2
    logging.info("dumping runway data")
    with open(f"{OUTPUT_FOLDER}/runway_list.json", "w") as f:
        json.dump(runway_list, f)
    with open(f"{OUTPUT_FOLDER}/runway_map.json", "w") as f:
        json.dump(runway_map, f)
    with open(f"{OUTPUT_FOLDER}/runway_split_map.json", "w") as f:
        json.dump(runway_split_map, f)


def generate_navaids():
    logging.info("loading and parsing navaids")
    navaids = parse_navaids()
    logging.info("generating navaid structures")
    navaid_list = []
    navaid_map = defaultdict(list)

    for nav in navaids:
        dump = nav.model_dump(exclude_none=True)
        navaid_list.append(dump)
        navaid_map[nav.ident].append(dump)

    logging.info("dumping navaid data")
    with open(f"{OUTPUT_FOLDER}/navaid_list.json", "w") as f:
        json.dump(navaid_list, f)
    with open(f"{OUTPUT_FOLDER}/navaid_map.json", "w") as f:
        json.dump(navaid_map, f)

    logging.info("generating navaid geojson")

    features = [nav.feature() for nav in navaids]
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    logging.info("dumping navaid geojson")
    with open(f"{OUTPUT_FOLDER}/navaid.geojson", "w") as f:
        json.dump(geojson, f)


def generate_regions():
    logging.info("loading and parsing regions")
    regions = parse_regions()
    logging.info("generating region list")
    region_list = [rgn.model_dump() for rgn in regions]
    logging.info("generating region map")
    region_map = {rgn.code: rgn.model_dump() for rgn in regions}
    logging.info("dumping airport data")
    with open(f"{OUTPUT_FOLDER}/region_list.json", "w") as f:
        json.dump(region_list, f)
    with open(f"{OUTPUT_FOLDER}/region_map.json", "w") as f:
        json.dump(region_map, f)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    generate_airports()
    generate_countries()
    generate_runways()
    generate_navaids()
    generate_regions()
