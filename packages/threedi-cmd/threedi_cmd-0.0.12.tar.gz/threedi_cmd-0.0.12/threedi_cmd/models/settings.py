from .base import SettingsWrapper
from openapi_client import SimulationsApi
from openapi_client.models import (
    PhysicalSettings,
    NumericalSettings,
    TimeStepSettings,
    AggregationSettings
)


class PhysicalSettingsWrapper(SettingsWrapper):
    api_class = SimulationsApi
    model = PhysicalSettings
    api_path: str = "physical"
    scenario_name = "physicalsettings"


class NumercialSettingsWrapper(SettingsWrapper):
    api_class = SimulationsApi
    model = NumericalSettings
    api_path: str = "numerical"
    scenario_name = "numericalsettings"


class TimeStepSettingsWrapper(SettingsWrapper):
    api_class = SimulationsApi
    model = TimeStepSettings
    api_path: str = "time_step"
    scenario_name = "timestepsettings"


class AggregationSettingsWrapper(SettingsWrapper):
    api_class = SimulationsApi
    model = AggregationSettings
    api_path: str = "aggregation"
    scenario_name = "aggregationsettings"


WRAPPERS = [
    PhysicalSettingsWrapper,
    NumercialSettingsWrapper,
    TimeStepSettingsWrapper,
    AggregationSettingsWrapper
]
