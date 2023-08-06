from dataclasses import dataclass, field
from enum import Enum
from dataclasses_json import dataclass_json
import typing as t

from tyba_client.utils import string_enum





@dataclass_json
@dataclass
class FixedTilt(object):
    tilt: float


@dataclass_json
@dataclass
class SingleAxisTracking(object):
    rotation_limit: float = 45.0
    backtrack: bool = True

@dataclass_json
@dataclass
class PVModel(object):
    location: t.Tuple[float, float]
    inverter_name: str
    pv_module_name: str
    gcr: float
    ac_capacity: float
    poi_limit: float
    dc_capacity: float
    tracking: t.Union[FixedTilt, SingleAxisTracking]
    # N.B. (Tyler) -- I copied these defaults from the production repo -- maybe these should just be optional
    # and we should rely on the defaults there, but this is the fastest option for now
    project_term: int = 1
    dc_degradation: float = 0.5

@dataclass_json
@dataclass
class SingleStorageInputs(object):
    power_capacity: float
    energy_capacity: float
    charge_efficiency: float
    discharge_efficiency: float
    degradation_rate: float
    cycling_cost_adder: t.Optional[float] = 0

@dataclass_json
@dataclass
class Battery(object):
    power_capacity: float
    energy_capacity: float
    charge_efficiency: float
    discharge_efficiency: float
    degradation_rate: float
    term: int

@dataclass_json
@dataclass
class StorageInputs(object):
    batteries: t.List[Battery]
    cycling_cost_adder: t.Optional[float] = 0



@dataclass_json
@dataclass
class StorageModel(object):
    storage_inputs: StorageInputs
    energy_prices: t.List[float]

@string_enum
class StorageCoupling(Enum):
    ac = 'ac'
    dc = 'dc'

@dataclass_json
@dataclass
class PVStorageModel(object):
    storage_coupling: StorageCoupling = field(metadata=StorageCoupling.__metadata__)
    pv_inputs: PVModel
    storage_inputs: StorageInputs
    energy_prices: t.List[float]