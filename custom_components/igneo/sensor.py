import logging
from datetime import timedelta
from tokenize import String
import traceback
from typing import Any, Callable, Dict, Optional
import json

from EstymaApiWrapper import EstymaApi

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_DEVICE_ID,
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT
)

from .const import *

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(seconds=30)

CONF_DEVICES = "devices"

IGNEO_DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.string,
        vol.Optional(CONF_NAME): cv.string
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_DEVICES): vol.All(cv.ensure_list,[IGNEO_DEVICE_SCHEMA])
    }
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    _LOGGER.critical("igneo entry")

async def async_setup_platform(hass: HomeAssistantType, config: ConfigType, async_add_entities: Callable, discovery_info: Optional[DiscoveryInfoType] = None,) -> None:
    """Set up the sensor platform."""
    _LOGGER.critical("igneo platform")

    Api = EstymaApi(config[CONF_USERNAME],config[CONF_PASSWORD])

    await Api.initialize()

    _LOGGER.critical("igneo platform: after init")
    
    sensors = [IgneoSensor(Api, device) for device in config[CONF_DEVICES]]
    async_add_entities(sensors, update_before_add=True)

class IgneoSensor(SensorEntity):

    def __init__(self, estymaapi: EstymaApi, device: Dict[str, str]) -> None:
        super().__init__()
        self._estymaapi = estymaapi
        self._name = device["name"]
        self._Device_Id = device["device_id"]
        self._state = None
        self._available = True
        self.attrs: Dict[str, Any] = {CONF_DEVICE_ID: self._Device_Id}

    @property
    def name(self) -> str:
        return self._name

    @property
    def unique_id(self) -> str:
        return self._Device_Id

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    @property
    def state(self) -> Optional[str]:
        return self._state

    async def async_update(self):
        if(self._estymaapi.initialized == False):
            _LOGGER.critical("igneo api not initialized")
            _LOGGER.critical(f'igneo api return code {self._estymaapi.returncode}')
            return

        try:
            _LOGGER.critical(f"updating {self._name} - {self._Device_Id}")
            devicedata = await self._estymaapi.getDeviceData(self._Device_Id)
            self.attrs[ATTR_consumption_fuel_total_current_sub1] = devicedata[f'{ATTR_consumption_fuel_total_current_sub1}']
            self.attrs[ATTR_temp_boiler_return_sub1] = devicedata[f'{ATTR_temp_boiler_return_sub1}']
            self.attrs[ATTR_temp_heating_curcuit1_sub1] = devicedata[f'{ATTR_temp_heating_curcuit1_sub1}']
            self.attrs[ATTR_temp_heating_curcuit2_sub1] = devicedata[f'{ATTR_temp_heating_curcuit2_sub1}']
            self.attrs[ATTR_temp_heating_curcuit3_sub1] = devicedata[f'{ATTR_temp_heating_curcuit3_sub1}']
            self.attrs[ATTR_temp_heating_curcuit4_sub1] = devicedata[f'{ATTR_temp_heating_curcuit4_sub1}']
            self.attrs[ATTR_power_output_boiler_sub1] = devicedata[f'{ATTR_power_output_boiler_sub1}']
            self.attrs[ATTR_lamda_pwm_sub1] = devicedata[f'{ATTR_lamda_pwm_sub1}']
            self.attrs[ATTR_temp_lamda_sub1] = devicedata[f'{ATTR_temp_lamda_sub1}']
            self.attrs[ATTR_temp_boiler_sub1] = devicedata[f'{ATTR_temp_boiler_sub1}']
            self.attrs[ATTR_temp_boiler_obli_sub1] = devicedata[f'{ATTR_temp_boiler_obli_sub1}']
            self.attrs[ATTR_temp_exhaust_boiler_sub1] = devicedata[f'{ATTR_temp_exhaust_boiler_sub1}']
            self.attrs[ATTR_oxygen_content_exhaust_sub1] = devicedata[f'{ATTR_oxygen_content_exhaust_sub1}']
            self.attrs[ATTR_status_burner_current_sub1] = devicedata[f'{ATTR_status_burner_current_sub1}']
            self.attrs[ATTR_fuel_fill_level_sub1] = devicedata[f'{ATTR_fuel_fill_level_sub1}']
            self.attrs[ATTR_temp_outside_sub1] = devicedata[f'{ATTR_temp_outside_sub1}']
            self.attrs[ATTR_energy_meter_sub1] = devicedata[f'{ATTR_energy_meter_sub1}']
            self.attrs[ATTR_status_boiler_pump_sub1] = devicedata[f'{ATTR_status_boiler_pump_sub1}']
            self.attrs[ATTR_sensor_type_circuit1_sub1] = devicedata[f'{ATTR_sensor_type_circuit1_sub1}']
            self.attrs[ATTR_target_temp_obw1_sub1] = devicedata[f'{ATTR_target_temp_obw1_sub1}']
            self.attrs[ATTR_status_pump_heating_curcuit1_sub1] = devicedata[f'{ATTR_status_pump_heating_curcuit1_sub1}']
            self.attrs[ATTR_temp_buffer_top_sub1] = devicedata[f'{ATTR_temp_buffer_top_sub1}']
            self.attrs[ATTR_temp_buffer_bottom_sub1] = devicedata[f'{ATTR_temp_buffer_bottom_sub1}']
            self.attrs[ATTR_device_type_sub1] = devicedata[f'{ATTR_device_type_sub1}']
            self.attrs[ATTR_number_obw_heating_curcuit_sub1] = devicedata[f'{ATTR_number_obw_heating_curcuit_sub1}']
            self.attrs[ATTR_number_obw_cwu_sub1] = devicedata[f'{ATTR_number_obw_cwu_sub1}']
            self.attrs[ATTR_number_buffers_sub1] = devicedata[f'{ATTR_number_buffers_sub1}']
            self.attrs[ATTR_status_solar_connected_sub1] = devicedata[f'{ATTR_status_solar_connected_sub1}']
            self.attrs[ATTR_state_lamda_sub1] = devicedata[f'{ATTR_state_lamda_sub1}']
            self.attrs[ATTR_temp_boiler_target_sub1] = devicedata[f'{ATTR_temp_boiler_target_sub1}']
            self.attrs[ATTR_temp_boiler_target_sub3] = devicedata[f'{ATTR_temp_boiler_target_sub3}']
            self.attrs[ATTR_temp_boiler_target_sub4] = devicedata[f'{ATTR_temp_boiler_target_sub4}']
        except:
            _LOGGER.exception("Shit hit the fan")
            _LOGGER.exception(traceback.print_exc())