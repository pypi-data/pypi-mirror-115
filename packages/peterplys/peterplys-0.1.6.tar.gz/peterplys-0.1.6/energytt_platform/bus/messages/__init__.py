from energytt_platform.bus import message_registry

from .auth import UserOnboarded
from .measurements import MeasurementAdded
from .meteringpoints import MeteringPointAdded, MeteringPointRemoved


message_registry.add(
    UserOnboarded,
    MeasurementAdded,
    MeteringPointAdded,
    MeteringPointRemoved,
)
