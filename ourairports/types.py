from typing import Optional, Any, List
from pydantic import BaseModel, field_validator


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
    keywords: List[str]

    @field_validator("elevation_ft", mode="before")
    @classmethod
    def convert_elevation(cls, v: Any) -> Optional[int]:
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator("keywords", mode="before")
    @classmethod
    def convert_keywords(cls, v: Any) -> List[str]:
        if v == '':
            return []
        return v.split(",")

    @field_validator("scheduled_service", mode="before")
    @classmethod
    def convert_scheduled_service(cls, v: Any) -> bool:
        return v == "yes"
