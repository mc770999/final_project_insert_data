from dataclasses import dataclass, field
from typing import List

@dataclass
class Location:
    country: str
    region: str
    city: str
    latitude: float
    longitude: float

    def __repr__(self):
        return (f"Location(country_name={self.country}, region={self.region}, "
                f"city={self.city}, latitude={self.latitude}, longitude={self.longitude})")
