from enum import Enum
from typing import Optional
from dataclasses import dataclass, field

from energytt_platform.serialize import Serializable


class Resolution(Enum):
    HOUR = 'HOUR'
    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'


@dataclass
class Address(Serializable):
    """
    TODO Which international standard does this convey to?
    """
    street_code: Optional[str] = field(default=None)
    street_name: Optional[str] = field(default=None)
    building_number: Optional[str] = field(default=None)
    floor_id: Optional[str] = field(default=None)
    room_id: Optional[str] = field(default=None)
    post_code: Optional[str] = field(default=None)
    city_name: Optional[str] = field(default=None)
    city_sub_division_name: Optional[str] = field(default=None)
    municipality_code: Optional[str] = field(default=None)
    location_description: Optional[str] = field(default=None)


@dataclass
class Technology(Serializable):
    """
    TODO Which international standard does this convey to?
    """
    technology_code: str
    fuel_code: str
    label: Optional[str] = field(default=None)
