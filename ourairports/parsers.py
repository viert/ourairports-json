import io
import requests
from typing import List, Generator, Dict, Any
from csv import DictReader
from ourairports.types import Airport, Country, Runway, NavAid


AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
NAV_AIDS_URL = "https://davidmegginson.github.io/ourairports-data/navaids.csv"
COUNTRIES_URL = "https://davidmegginson.github.io/ourairports-data/countries.csv"
REGIONS_URL = "https://davidmegginson.github.io/ourairports-data/regions.csv"
RUNWAYS_URL = "https://davidmegginson.github.io/ourairports-data/runways.csv"


def load(url: str) -> Generator[Dict[str, Any], None, None]:
    data = requests.get(url)
    rdr = io.StringIO(data.text)
    csv_rdr = DictReader(rdr)
    for row in csv_rdr:
        yield row


def parse_airports() -> List[Airport]:
    airports = [Airport(**row) for row in load(AIRPORTS_URL)]
    airports.sort(key=lambda x: x.id)
    return airports


def parse_countries() -> List[Country]:
    countries = [Country(**row) for row in load(COUNTRIES_URL)]
    countries.sort(key=lambda x: x.id)
    return countries


def parse_runways() -> List[Runway]:
    runways = [Runway(**rwy) for rwy in load(RUNWAYS_URL)]
    runways.sort(key=lambda x: x.id)
    return runways


def parse_navaids() -> List[NavAid]:
    navaids = [NavAid(**row) for row in load(NAV_AIDS_URL)]
    navaids.sort(key=lambda x: x.id)
    return navaids
