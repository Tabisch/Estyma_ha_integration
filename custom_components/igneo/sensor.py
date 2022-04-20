import logging
from datetime import timedelta
from tokenize import String
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
    sensors = [IgneoSensor(Api, device) for device in config[CONF_DEVICES]]
    async_add_entities(sensors, update_before_add=True)

class IgneoSensor(SensorEntity):

    def __init__(self, estymaapi, device) -> None:
        super().__init__()
        self.estymaapi = estymaapi
        self._name = device["name"]
        self._Device_Id = f'{device["device_id"]}-'
        self._available = True

    @property
    def name(self) -> str:
        return self._name

    @property
    def unique_id(self) -> str:
        return self._Device_Id

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    @property
    def state(self) -> Optional[str]:
        return self._state

    async def async_update(self):
        try:
            devicedata = json.loads(self.estymaapi.fetchDevicedata(self._Device_Id))
            self.attrs[ATTR_consumption_fuel_total_current_sub1] = devicedata["ATTR_consumption_fuel_total_current_sub1"]
            #self.attrs[] =
        except Exception:
            _LOGGER.exception("Shit hit the fan")