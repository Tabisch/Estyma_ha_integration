import asyncio
from datetime import timedelta
import logging
import traceback
from typing import Any, Callable, Optional

from EstymaApiWrapper import EstymaApi
import voluptuous as vol

from homeassistant.components.select import PLATFORM_SCHEMA, SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE_ID, CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DEFAULT_NAME,
    DOMAIN,
    ATTR_language,
    ATTR_temp_boiler_target_sub1,
    ATTR_operation_mode_boiler_sub1,
    ATTR_target_temp_buffer_top_sub1,
    ATTR_target_temp_buffer_bottom_sub1,
    ATTR_target_temp_room_comf_heating_curcuit_sub1,
    ATTR_target_temp_room_eco_heating_curcuit_sub1,
    ATTR_heating_curcuit_prog_obw1_sub1,
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


async def setup(coordinator: CoordinatorEntity):
    _LOGGER.debug(f"Setting up selectss - Devices: {coordinator.data.keys()}")

    sensors = []
    # ToDo cleanup
    for device_id in list(coordinator.data.keys()):
        sensors.append(
            EstymaSelectEntity(
                coordinator=coordinator,
                deviceAttribute=ATTR_operation_mode_boiler_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSelectEntity(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_boiler_target_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSelectEntity(
                coordinator=coordinator,
                deviceAttribute=ATTR_target_temp_buffer_top_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSelectEntity(
                coordinator=coordinator,
                deviceAttribute=ATTR_target_temp_buffer_bottom_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSelectEntity(
                coordinator=coordinator,
                deviceAttribute=ATTR_target_temp_room_comf_heating_curcuit_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSelectEntity(
                coordinator=coordinator,
                deviceAttribute=ATTR_target_temp_room_eco_heating_curcuit_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSelectEntity(
                coordinator=coordinator,
                deviceAttribute=ATTR_heating_curcuit_prog_obw1_sub1,
                Device_Id=device_id,
            )
        )

    return sensors


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


class EstymaSelectEntity(SelectEntity, CoordinatorEntity):
    def __init__(
        self, coordinator: CoordinatorEntity, deviceAttribute, Device_Id
    ) -> None:
        super().__init__(coordinator=coordinator)
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute

        self._optionDisplayToRealValueTable = {}

        _optionsList = list()
        for key in self.coordinator.availableSettings[Device_Id][
            self._attributename
        ].keys():
            _optionsList.append(
                str(
                    self.coordinator.availableSettings[Device_Id][self._attributename][
                        key
                    ]["name"]
                )
            )
            self._optionDisplayToRealValueTable[
                str(
                    self.coordinator.availableSettings[Device_Id][self._attributename][
                        key
                    ]["name"]
                )
            ] = key

        self._attr_current_option = str(
            self.coordinator.data[Device_Id][self._attributename]
        )
        self._attr_options = _optionsList
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
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, f"{DEFAULT_NAME}_{self.attrs[CONF_DEVICE_ID]}")
            },
            "name": f"{DEFAULT_NAME}_{self.attrs[CONF_DEVICE_ID]}",
            "manufacturer": DEFAULT_NAME,
        }

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if self.coordinator.UpdatingSettingTable[self.attrs[CONF_DEVICE_ID]][
            self._attributename
        ]:
            _LOGGER.debug(
                f"EstymaSelectEntity async_select_option - {self._name} - {self.attrs[CONF_DEVICE_ID]} - update disabled"
            )
            return
        else:
            _LOGGER.debug(
                f"EstymaSelectEntity async_select_option - {self._name} - {self.attrs[CONF_DEVICE_ID]} - {option}"
            )

            await self.coordinator.api.changeSetting(
                self.attrs[CONF_DEVICE_ID],
                self._attributename,
                self._optionDisplayToRealValueTable[option],
            )

            self._attr_current_option = option

            self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        if self.coordinator.UpdatingSettingTable[self.attrs[CONF_DEVICE_ID]][
            self._attributename
        ]:
            _LOGGER.debug(
                f"EstymaSelectEntity - {self._name} - {self.attrs[CONF_DEVICE_ID]} - updating is disabled"
            )
        else:
            _LOGGER.debug(
                f"EstymaSelectEntity - {self._name} - {self.attrs[CONF_DEVICE_ID]} - {self.coordinator.dataTextToValues[self.attrs[CONF_DEVICE_ID]][
                    self._attributename
                ]}"
            )

            self._attr_current_option = str(
                self.coordinator.data[self.attrs[CONF_DEVICE_ID]][self._attributename]
            )

            self.async_write_ha_state()
