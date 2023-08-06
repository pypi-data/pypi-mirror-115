from datetime import datetime
from dataclasses import dataclass

from energytt_platform.serialize import Serializable

from .common import EnergyDirection


MeasurementType = EnergyDirection


@dataclass
class Measurement(Serializable):
    gsrn: str
    amount: int
    begin: datetime
    end: datetime
    type: MeasurementType
