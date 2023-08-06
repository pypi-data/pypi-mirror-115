from enum import Enum
from typing import Optional
from dataclasses import dataclass, field

from energytt_platform.serialize import Serializable


class TechnologyLabel(Enum):
    """
    System-wide labels of known technologies.
    """
    COAL = 'Coal'
    NUCLEAR = 'Nuclear'
    SOLAR = 'Solar'
    WIND = 'Wind'


@dataclass
class Technology(Serializable):
    """
    A technology described by the standard described in the
    EECS Rules Fact Sheet 5: TYPES OF ENERGY INPUTS AND TECHNOLOGIES
    """
    technology_code: str
    fuel_code: str
    label: Optional[TechnologyLabel] = field(default=None)  # TODO Why optional ???
