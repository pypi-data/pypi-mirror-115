from typing import Optional
from dataclasses import dataclass, field

from energytt_platform.bus import Message
from energytt_platform.models.common import Address
from energytt_platform.models.technologies import Technology
from energytt_platform.models.meteringpoints import \
    MeteringPoint, MeteringPointType


@dataclass
class MeteringPointAdded(Message):
    """
    A new MeteringPoint has been added to the system.
    """
    subject: str
    meteringpoint: MeteringPoint


@dataclass
class MeteringPointRemoved(Message):
    """
    A MeteringPoint has been remove from the system.
    """
    gsrn: str


@dataclass
class MeteringPointMetaDataUpdate(Message):
    """
    Metadata for a MeteringPoint has been updated.
    """
    gsrn: str
    type: Optional[MeteringPointType] = field(default=None)
    technology: Optional[Technology] = field(default=None)
    address: Optional[Address] = field(default=None)
