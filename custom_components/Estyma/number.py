import asyncio
import logging
from datetime import timedelta, datetime
import traceback
from typing import Any, Callable, Dict, Optional

from EstymaApiWrapper import EstymaApi

import voluptuous as vol

from homeassistant.components.number import PLATFORM_SCHEMA, NumberEntity, NumberEntityDescription, RestoreNumber
from homeassistant.components.number.const import MODE_BOX
from homeassistant.config_entries import ConfigEntry
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
    PERCENTAGE,
    TEMP_CELSIUS,
    MASS_KILOGRAMS,
    ENERGY_KILO_WATT_HOUR,
    ENERGY_MEGA_WATT_HOUR,
    ENERGY_WATT_HOUR
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

    _LOGGER.debug("Setting up sensors")

    while(Api.initialized == False):
        await Api.initialize(throw_Execetion= False)
        if(Api.initialized == False):
            break
        else:
            await asyncio.sleep(_failedInitSleepTime)

    defaultDescription = NumberEntityDescription(
        key="default",
        native_max_value=9999999,
        native_min_value=0,
        native_step=1,
        mode=MODE_BOX
    )

    sensors = []
    #ToDo cleanup
    for device_id in list(Api.devices.keys()):
        sensors.append(EstymaNumber(defaultDescription, ATTR_last_empty_weight, device_id, MASS_KILOGRAMS))
        sensors.append(EstymaNumber(defaultDescription, ATTR_last_empty_weight_offset, device_id, MASS_KILOGRAMS))

    return sensors

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    config = hass.data[DOMAIN][entry.entry_id]

    _estymaApi = EstymaApi(Email= config[CONF_EMAIL], Password= config[CONF_PASSWORD], scanInterval= 0, language= config[ATTR_language])
    
    async_add_entities(await setup(Api= _estymaApi), update_before_add=True)

async def async_setup_platform(hass: HomeAssistantType, config: ConfigType, async_add_entities: Callable, discovery_info: Optional[DiscoveryInfoType] = None,) -> None:
    """Set up the sensor platform."""
    _estymaApi = EstymaApi(Email= config[CONF_EMAIL], Password= config[CONF_PASSWORD], scanInterval= 0, language= config[ATTR_language])
    
    async_add_entities(await setup(Api= _estymaApi), update_before_add=True)

class EstymaNumber(RestoreNumber, NumberEntity):

    def __init__(self, description: NumberEntityDescription, deviceAttribute, Device_Id, native_unit_of_measurement = None) -> None:
        super().__init__()
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self.entity_description = description

        if(native_unit_of_measurement != None):
            self._attr_native_unit_of_measurement = native_unit_of_measurement

        self._state = None
        self._available = True

        self.attrs: Dict[str, Any] = {
            CONF_DEVICE_ID: Device_Id
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
    def state(self) -> Optional[str]:
        return self._state
    
    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._state = value

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
    
    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if not state:
            return
        self._state = state.state