from enum import Enum
from typing import Optional
from dataclasses import dataclass, field

from energytt_platform.serialize import Serializable

from .common import Address, Technology


class MeteringPointType(Enum):
    PRODUCTION = 'PRODUCTION'  # E18
    CONSUMPTION = 'CONSUMPTION'  # E17


@dataclass
class MeteringPoint(Serializable):
    """
    A single Metering Point.

    TODO Add physical address
    """
    gsrn: str
    sector: str
    type: Optional[MeteringPointType] = field(default=None)
    technology: Optional[Technology] = field(default=None)
    address: Optional[Address] = field(default=None)


@dataclass
class MeteringPointMetaData(Serializable):
    """
    MeteringPoint meta data.

    TODO Add physical address
    """
    gsrn: str
    type: Optional[MeteringPointType] = field(default=None)
    technology: Optional[Technology] = field(default=None)
    address: Optional[Address] = field(default=None)
