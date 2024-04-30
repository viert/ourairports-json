from typing import Optional, List, Callable, Annotated, Dict, Any, Tuple
from pydantic import BaseModel, ValidationInfo, BeforeValidator


def make_bool_converter(true_value: str) -> Callable[[str, ValidationInfo], bool]:
    def converter(v: str | bool, _: ValidationInfo) -> bool:
        if isinstance(v, bool):
            return v
        return v == true_value
    return converter


def csl_converter(v: List | str, _: ValidationInfo) -> List[str]:
    if isinstance(v, list):
        return v
    if v.strip() == "":
        return []
    return [x.strip() for x in v.split(",")]


def try_int_converter(v: str | int, _: ValidationInfo) -> Optional[int]:
    if isinstance(v, int):
        return v
    if v is None or v == "":
        return None
    try:
        return int(v)
    except ValueError:
        return None


def non_empty_str_or_null(v: str | None, _: ValidationInfo) -> Optional[str]:
    if v is None or v == "":
        return None
    return v


def try_float_converter(v: str | float, _: ValidationInfo) -> Optional[float]:
    if isinstance(v, float):
        return v
    if v is None or v == "":
        return None
    try:
        return float(v)
    except ValueError:
        return None


class Airport(BaseModel):
    id: int
    ident: str
    type: str
    name: str
    latitude_deg: float
    longitude_deg: float
    elevation_ft: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    continent: str
    iso_country: str
    iso_region: str
    municipality: str
    scheduled_service: Annotated[bool, BeforeValidator(make_bool_converter("yes"))]
    gps_code: str
    iata_code: str
    local_code: str
    home_link: str
    wikipedia_link: str
    keywords: Annotated[List[str], BeforeValidator(csl_converter)]


class AirportExtFreq(BaseModel):
    type: str
    description: str
    frequency_mhz: float


class AirportFrequency(AirportExtFreq):
    id: int
    airport_ref: int
    airport_ident: str

    def to_ext(self) -> AirportExtFreq:
        return AirportExtFreq(type=self.type, description=self.description, frequency_mhz=self.frequency_mhz)


class AirportExtended(Airport):
    frequencies: Optional[Dict[str, List[AirportExtFreq]]] = None


class Country(BaseModel):
    id: int
    code: str
    name: str
    continent: str
    wikipedia_link: str
    keywords: Annotated[List[str], BeforeValidator(csl_converter)]


class SplitRunway(BaseModel):
    airport_ref: int
    airport_ident: str
    length_ft: Optional[int]
    width_ft: Optional[int]
    surface: str
    lighted: bool
    closed: bool
    ident: str
    latitude_deg: Optional[float]
    longitude_deg: Optional[float]
    elevation_ft: Optional[int]
    heading_degT: Optional[int]
    displaced_threshold_ft: Optional[int]


class Runway(BaseModel):
    id: int
    airport_ref: int
    airport_ident: str
    length_ft: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    width_ft: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    surface: str
    lighted: bool
    closed: bool
    le_ident: str
    le_latitude_deg: Annotated[Optional[float], BeforeValidator(try_float_converter)]
    le_longitude_deg: Annotated[Optional[float], BeforeValidator(try_float_converter)]
    le_elevation_ft: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    le_heading_degT: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    le_displaced_threshold_ft: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    he_ident: str
    he_latitude_deg: Annotated[Optional[float], BeforeValidator(try_float_converter)]
    he_longitude_deg: Annotated[Optional[float], BeforeValidator(try_float_converter)]
    he_elevation_ft: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    he_heading_degT: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    he_displaced_threshold_ft: Annotated[Optional[int], BeforeValidator(try_int_converter)]

    def split(self) -> Tuple[SplitRunway, SplitRunway]:
        return (
            SplitRunway(
                airport_ref=self.airport_ref,
                airport_ident=self.airport_ident,
                length_ft=self.length_ft,
                width_ft=self.width_ft,
                surface=self.surface,
                lighted=self.lighted,
                closed=self.closed,
                ident=self.le_ident,
                latitude_deg=self.le_latitude_deg,
                longitude_deg=self.le_longitude_deg,
                elevation_ft=self.le_elevation_ft,
                heading_degT=self.le_heading_degT,
                displaced_threshold_ft=self.le_displaced_threshold_ft
            ),
            SplitRunway(
                airport_ref=self.airport_ref,
                airport_ident=self.airport_ident,
                length_ft=self.length_ft,
                width_ft=self.width_ft,
                surface=self.surface,
                lighted=self.lighted,
                closed=self.closed,
                ident=self.he_ident,
                latitude_deg=self.he_latitude_deg,
                longitude_deg=self.he_longitude_deg,
                elevation_ft=self.he_elevation_ft,
                heading_degT=self.he_heading_degT,
                displaced_threshold_ft=self.he_displaced_threshold_ft
            ),
        )

class NavAid(BaseModel):
    id: int
    ident: str
    name: str
    type: str
    frequency_khz: int
    latitude_deg: float
    longitude_deg: float
    elevation_ft: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    iso_country: str
    dme_frequency_khz: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    dme_channel: Annotated[Optional[str], BeforeValidator(non_empty_str_or_null)]
    dme_latitude_deg: Annotated[Optional[float], BeforeValidator(try_float_converter)]
    dme_longitude_deg: Annotated[Optional[float], BeforeValidator(try_float_converter)]
    dme_elevation_ft: Annotated[Optional[int], BeforeValidator(try_int_converter)]
    slaved_variation_deg: Annotated[Optional[float], BeforeValidator(try_float_converter)]
    magnetic_variation_deg: Annotated[Optional[float], BeforeValidator(try_float_converter)]
    usageType: Annotated[Optional[str], BeforeValidator(non_empty_str_or_null)]
    power: Annotated[Optional[str], BeforeValidator(non_empty_str_or_null)]
    associated_airport: Annotated[Optional[str], BeforeValidator(non_empty_str_or_null)]

    def feature(self) -> Dict[str, Any]:
        props = {
            "ident": self.ident,
            "name": self.name,
            "type": self.type,
            "frequency_khz": self.frequency_khz
        }

        extra_props = [
            "elevation_ft",
            "dme_frequency_khz",
            "dme_channel",
            "dme_latitude_deg",
            "dme_longitude_deg",
            "slaved_variation_deg",
            "magnetic_variation_deg",
            "usageType",
            "power",
            "associated_airport",
        ]

        for prop in extra_props:
            prop_value = getattr(self, prop, None)
            if prop_value is not None:
                props[prop] = prop_value

        return {
            "id": self.id,
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.longitude_deg, self.latitude_deg]
            },
            "properties": props
        }


class Region(BaseModel):
    id: int
    code: str
    local_code: str
    name: str
    continent: str
    iso_country: str
    wikipedia_link: str
    keywords: Annotated[List[str], BeforeValidator(csl_converter)]
