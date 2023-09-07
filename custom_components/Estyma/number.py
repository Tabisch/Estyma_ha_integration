import asyncio
import logging
from datetime import timedelta
import traceback
from typing import Any, Callable, Dict, Optional

from EstymaApiWrapper import EstymaApi

import voluptuous as vol

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA
from homeassistant.components.number import NumberEntity
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
    CONF_DEVICE_ID,
    TEMP_CELSIUS
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
        settings = await Api.getAvailableSettings(device_id)
        sensors.append(EstymaNumberEntity(Api, ATTR_temp_boiler_target_sub1, device_id, TEMP_CELSIUS, settings))
        sensors.append(EstymaNumberEntity(Api, ATTR_target_temp_buffer_top_sub1, device_id, TEMP_CELSIUS, settings))
        sensors.append(EstymaNumberEntity(Api, ATTR_target_temp_buffer_bottom_sub1, device_id, TEMP_CELSIUS, settings))
        sensors.append(EstymaNumberEntity(Api, ATTR_target_temp_room_comf_heating_curcuit_sub1, device_id, TEMP_CELSIUS, settings))
        sensors.append(EstymaNumberEntity(Api, ATTR_target_temp_room_eco_heating_curcuit_sub1, device_id, TEMP_CELSIUS, settings))
    return sensors

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    config = hass.data[DOMAIN][entry.entry_id]

    _estymaApi = EstymaApi(Email= config[CONF_EMAIL], Password= config[CONF_PASSWORD], scanInterval= 0, language= config[ATTR_language])
    
    async_add_entities(await setup(Api= _estymaApi), update_before_add=True)

async def async_setup_platform(hass: HomeAssistantType, config: ConfigType, async_add_entities: Callable, discovery_info: Optional[DiscoveryInfoType] = None,) -> None:
    """Set up the sensor platform."""
    _estymaApi = EstymaApi(Email= config[CONF_EMAIL], Password= config[CONF_PASSWORD], scanInterval= 0, language= config[ATTR_language])
    
    async_add_entities(await setup(Api= _estymaApi), update_before_add=True)

class EstymaNumberEntity(NumberEntity):

    def __init__(self, estymaapi: EstymaApi, deviceAttribute, Device_Id, native_unit_of_measurement = None, settings = None) -> None:
        super().__init__()
        self._estymaapi = estymaapi
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute
        self._enabled = True

        settingsKeys = settings[deviceAttribute].keys()
        settingsAttribute = settings[deviceAttribute]

        if settings:
            for key in settingsKeys:
                if settingsAttribute[key]["selected"] == True:
                    self._native_value = int(settingsAttribute[key]["name"])

            self._native_min_value = int(settingsAttribute[0]["name"])
            self._native_max_value = int(settingsAttribute[len(settingsKeys) - 1]["name"])
            self._native_step = int(settingsAttribute[1]["name"]) - int(settingsAttribute[0]["name"])
        else:
            self._enabled = False

        if(native_unit_of_measurement != None):
            self._attr_native_unit_of_measurement = native_unit_of_measurement

        self._available = True
        self.attrs: Dict[str, Any] = {
            CONF_DEVICE_ID: Device_Id,
            "last_update": "",
            "last_update_diff": ""
        }

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
    def enabled(self) -> bool:
        return self._enabled

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs
    
    @property
    def native_value(self) -> float | int | None:
        return self._native_value
    
    @property
    def native_min_value(self) -> float | int | None:
        return self._native_min_value
    
    @property
    def native_max_value(self) -> float | int | None:
        return self._native_max_value
    
    @property
    def native_step(self) -> float | int | None:
        return self._native_step

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

    async def async_update(self):
        _LOGGER.warn(f"updating {self._name} - {self.attrs[CONF_DEVICE_ID]}")

        #while(self._estymaapi.updatingData == True):
        #    _LOGGER.debug(f"waiting for update to finish {self._name} - {self.attrs[CONF_DEVICE_ID]}")
        #    asyncio.sleep(1)

        try:
            data = await self._estymaapi.getDeviceData(self.attrs[CONF_DEVICE_ID])

            self._state = data[self._attributename]

            self.attrs["last_update"] = data["online"]["last_date"]
            self.attrs["last_update_diff"] = data["online"]["diff"]
        except:
            _LOGGER.exception(traceback.print_exc())

    async def async_set_native_value(self, value: float) -> None:
        self._native_value = value