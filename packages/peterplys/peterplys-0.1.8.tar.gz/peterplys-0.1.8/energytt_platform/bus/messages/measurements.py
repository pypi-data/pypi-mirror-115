from dataclasses import dataclass

from energytt_platform.bus import Message
from energytt_platform.models.measurements import Measurement


@dataclass
class MeasurementAdded(Message):
    """
    A new Measurement has been added to the system.
    """
    subject: str
    measurement: Measurement
