from dataclasses import dataclass

from energytt_platform.bus import Message
from energytt_platform.models.technologies import Technology


@dataclass
class TechnologyUpdate(Message):
    """
    An update to a Technology.
    """
    technology: Technology
