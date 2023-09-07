import io
import requests
from typing import List
from csv import DictReader
from ourairports.types import Airport


AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"


def parse_airports() -> List[Airport]:
    data = requests.get(AIRPORTS_URL)
    rdr = io.StringIO(data.text)
    csv_rdr = DictReader(rdr)
    airports = [Airport(**row) for row in csv_rdr]
    airports.sort(key=lambda x: x.id)
    return airports
