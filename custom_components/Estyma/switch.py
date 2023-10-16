import asyncio
import logging
from datetime import timedelta
import traceback
from typing import Any, Callable, Dict, Optional

from EstymaApiWrapper import EstymaApi

import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

from homeassistant.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_DEVICE_ID
)

from .const import *

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(seconds=30)
_failedInitSleepTime = 5

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(ATTR_language): cv.string
    }
)

async def setup(Api: EstymaApi):
    while(Api.initialized == False):
        await Api.initialize(throw_Execetion= False)
        if(Api.initialized == False):
            break
        else:
            await asyncio.sleep(_failedInitSleepTime)

    sensors = []
    #ToDo cleanup
    for device_id in list(Api.devices.keys()):
        sensors.append(EstymaBinarySwitch(Api, ATTR_status_controller_sub1, device_id))

    return sensors

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    config = hass.data[DOMAIN][entry.entry_id]

    _estymaApi = EstymaApi(Email= config[CONF_EMAIL], Password= config[CONF_PASSWORD], scanInterval= 0, language= config[ATTR_language])
    
    async_add_entities(await setup(Api= _estymaApi), update_before_add=True)

async def async_setup_platform(hass: HomeAssistantType, config: ConfigType, async_add_entities: Callable, discovery_info: Optional[DiscoveryInfoType] = None,) -> None:
    """Set up the sensor platform."""
    _estymaApi = EstymaApi(Email= config[CONF_EMAIL], Password= config[CONF_PASSWORD], scanInterval= 0, language= config[ATTR_language])
    
    async_add_entities(await setup(Api= _estymaApi), update_before_add=True)

class EstymaBinarySwitch(SwitchEntity):

    def __init__(self, estymaapi: EstymaApi, deviceAttribute, Device_Id) -> None:
        super().__init__()
        self._estymaapi = estymaapi
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute

        self._state = None
        self._available = True

    @property
    def name(self) -> str:
        return self._name

    # Todo automatic names
    #@property
    #def displayname(self):
    #    return "text"

    @property
    def unique_id(self) -> str:
        return f"{self._name}"

    @property
    def is_on(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, f"{DEFAULT_NAME}_{self.attrs[CONF_DEVICE_ID]}")
            },
            "name": f"{DEFAULT_NAME}_{self.attrs[CONF_DEVICE_ID]}",
            "manufacturer": DEFAULT_NAME,
        }
    
    async def async_turn_on(self):
        """Turn the entity on."""
    
    async def async_turn_off(self):
        """Turn the entity off."""

    async def async_toggle(self):
        """Toggle the entity."""

    async def async_update(self):
        _LOGGER.debug(f"updating {self._name} - {self.attrs[CONF_DEVICE_ID]}")

        try:
            data = await self._estymaapi.getDeviceData(self.attrs[CONF_DEVICE_ID])

            self._state = data[self._attributename]
        except:
            _LOGGER.exception(traceback.print_exc())