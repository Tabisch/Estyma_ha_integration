import asyncio
from datetime import timedelta
import logging
import traceback
from typing import Any, Callable, Optional

from EstymaApiWrapper import EstymaApi
import voluptuous as vol

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE_ID, CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    DEFAULT_NAME,
    DOMAIN,
    ATTR_burner_enabled_sub1,
    ATTR_dataUpToDate,
    ATTR_language,
    ATTR_status_boiler_pump_sub1,
    ATTR_status_pump_heating_curcuit1_sub1,
)

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(seconds=30)
_failedInitSleepTime = 5

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(ATTR_language): cv.string,
    }
)


async def setup(Api: EstymaApi):
    _LOGGER.debug("Setting up binary_sensors")

    while Api.initialized is False:
        await Api.initialize(throw_Execetion=False)
        if Api.initialized is False:
            break

        await asyncio.sleep(_failedInitSleepTime)

    sensors = []
    # ToDo cleanup
    for device_id in list(Api.devices.keys()):
        sensors.append(EstymaBinarySensor(Api, ATTR_dataUpToDate, device_id))
        sensors.append(EstymaBinarySensor(Api, ATTR_burner_enabled_sub1, device_id))
        sensors.append(
            EstymaBinarySensor(Api, ATTR_status_pump_heating_curcuit1_sub1, device_id)
        )
        sensors.append(EstymaBinarySensor(Api, ATTR_status_boiler_pump_sub1, device_id))

    return sensors


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    config = hass.data[DOMAIN][entry.entry_id]

    _estymaApi = EstymaApi(
        Email=config[CONF_EMAIL],
        Password=config[CONF_PASSWORD],
        scanInterval=0,
        language=config[ATTR_language],
    )

    async_add_entities(await setup(Api=_estymaApi), update_before_add=True)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the sensor platform."""
    _estymaApi = EstymaApi(
        Email=config[CONF_EMAIL],
        Password=config[CONF_PASSWORD],
        scanInterval=0,
        language=config[ATTR_language],
    )

    async_add_entities(await setup(Api=_estymaApi), update_before_add=True)


class EstymaBinarySensor(BinarySensorEntity):
    def __init__(self, estymaapi: EstymaApi, deviceAttribute, Device_Id) -> None:
        super().__init__()
        self._estymaapi = estymaapi
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute

        self._state = None
        self._available = True

        self.attrs: dict[str, Any] = {
            CONF_DEVICE_ID: Device_Id,
            "last_update": "",
            "last_update_diff": "",
        }

    @property
    def name(self) -> str:
        return self._name

    # Todo automatic names
    # @property
    # def displayname(self):
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

    async def async_update(self):
        _LOGGER.debug(f"updating {self._name} - {self.attrs[CONF_DEVICE_ID]}")

        # while(self._estymaapi.updatingData == True):
        #    _LOGGER.debug(f"waiting for update to finish {self._name} - {self.attrs[CONF_DEVICE_ID]}")
        #    asyncio.sleep(1)

        try:
            data = await self._estymaapi.getDeviceData(
                self.attrs[CONF_DEVICE_ID], textToValues=True
            )

            self._state = data[self._attributename]
        except:
            _LOGGER.exception(traceback.print_exc())
