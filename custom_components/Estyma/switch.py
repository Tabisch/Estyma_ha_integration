import asyncio
from datetime import timedelta
import logging
import traceback
from typing import Any, Callable, Optional

from EstymaApiWrapper import EstymaApi
import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE_ID, CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_NAME, DOMAIN, ATTR_language, ATTR_status_controller_sub1

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


async def setup(coordinator: CoordinatorEntity):
    _LOGGER.debug(f"Setting up switches - Devices: {coordinator.data.keys()}")

    switches = []
    # ToDo cleanup
    for device_id in list(coordinator.data.keys()):
        switches.append(
            EstymaBinarySwitch(
                coordinator=coordinator,
                deviceAttribute=ATTR_status_controller_sub1,
                Device_Id=device_id,
            )
        )

    return switches


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = entry.runtime_data

    async_add_entities(await setup(coordinator=coordinator), update_before_add=True)


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


class EstymaBinarySwitch(SwitchEntity, CoordinatorEntity):
    def __init__(
        self, coordinator: CoordinatorEntity, deviceAttribute, Device_Id
    ) -> None:
        super().__init__(coordinator=coordinator)
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute

        self._state = bool(
            self.coordinator.dataTextToValues[Device_Id][self._attributename]
        )

        self._available = True

        self.attrs: dict[str, Any] = {
            CONF_DEVICE_ID: Device_Id,
            "last_update": "",
            "last_update_diff": "",
        }

        _LOGGER.debug(f"Setup complete {self._name} - {self.attrs[CONF_DEVICE_ID]}")

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

    async def async_turn_on(self):
        """Turn the entity on."""
        if self.coordinator.UpdatingSettingTable[self.attrs[CONF_DEVICE_ID]][
            self._attributename
        ]:
            _LOGGER.debug(
                f"turning on disabled - entity is updating {self._name} - {self.attrs[CONF_DEVICE_ID]}"
            )
            return
        else:
            _LOGGER.debug(f"turning on {self._name} - {self.attrs[CONF_DEVICE_ID]}")

        await self.coordinator.api.changeSetting(
            self.attrs[CONF_DEVICE_ID], self._attributename, 1
        )

        self._state = True

        self.async_write_ha_state()

    async def async_turn_off(self):
        """Turn the entity off."""
        if self.coordinator.UpdatingSettingTable[self.attrs[CONF_DEVICE_ID]][
            self._attributename
        ]:
            _LOGGER.debug(
                f"turning off disabled - entity is updating {self._name} - {self.attrs[CONF_DEVICE_ID]}"
            )
            return
        else:
            _LOGGER.debug(f"turning off {self._name} - {self.attrs[CONF_DEVICE_ID]}")

        await self.coordinator.api.changeSetting(
            self.attrs[CONF_DEVICE_ID], self._attributename, 0
        )

        self._state = False

        self.async_write_ha_state()

    async def async_toggle(self):
        """Toggle the entity."""
        _LOGGER.debug(f"toggleing {self._name} - {self.attrs[CONF_DEVICE_ID]}")

        if self._state:
            self.async_turn_off()
        else:
            self.async_turn_on()

    @callback
    def _handle_coordinator_update(self) -> None:
        if self.coordinator.UpdatingSettingTable[self.attrs[CONF_DEVICE_ID]][
            self._attributename
        ]:
            _LOGGER.debug(
                f"EstymaBinarySwitch - {self._name} - {self.attrs[CONF_DEVICE_ID]} - updating is disabled"
            )
        else:
            _LOGGER.debug(
                f"EstymaBinarySwitch - {self._name} - {self.attrs[CONF_DEVICE_ID]} - {self.coordinator.dataTextToValues[self.attrs[CONF_DEVICE_ID]][
                    self._attributename
                ]}"
            )

            self._state = bool(
                self.coordinator.dataTextToValues[self.attrs[CONF_DEVICE_ID]][
                    self._attributename
                ]
            )

            self.async_write_ha_state()
