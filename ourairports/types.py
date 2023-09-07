from typing import Optional, Any, List, Callable, Annotated
from pydantic import BaseModel, field_validator, ValidationInfo, BeforeValidator


def make_csl_converter(label: str) -> Callable[[str, ValidationInfo], List[str]]:
    def converter(v: str, info: ValidationInfo) -> List[str]:
        if v.strip() == "":
            return []
        return [x.strip() for x in v.split(",")]
    return converter


class Airport(BaseModel):
    id: int
    ident: str
    type: str
    name: str
    latitude_deg: float
    longitude_deg: float
    elevation_ft: Optional[int]
    continent: str
    iso_country: str
    iso_region: str
    municipality: str
    scheduled_service: bool
    gps_code: str
    iata_code: str
    local_code: str
    home_link: str
    wikipedia_link: str
    keywords: Annotated[List[str], BeforeValidator(make_csl_converter("keywords"))]

    @field_validator("elevation_ft", mode="before")
    @classmethod
    def convert_elevation(cls, v: Any) -> Optional[int]:
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator("scheduled_service", mode="before")
    @classmethod
    def convert_scheduled_service(cls, v: Any) -> bool:
        return v == "yes"


class Country(BaseModel):
    id: int
    code: str
    name: str
    continent: str
    wikipedia_link: str
    keywords: Annotated[List[str], BeforeValidator(make_csl_converter("keywords"))]
