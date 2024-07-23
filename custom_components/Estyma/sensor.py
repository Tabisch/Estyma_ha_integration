import asyncio
import json
from datetime import datetime, timedelta
import logging
import traceback
from typing import Any, Callable, Dict, Optional

from EstymaApiWrapper import EstymaApi
import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_EMAIL,
    CONF_PASSWORD,
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfMass,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DEFAULT_NAME,
    DOMAIN,
    ATTR_consumption_fuel_current_day,
    ATTR_consumption_fuel_total_current_sub1,
    ATTR_current_status_burner_sub1,
    ATTR_current_status_burner_sub1_int,
    ATTR_daily_energy,
    ATTR_energy_meter_sub1,
    ATTR_fuel_fill_level_sub1,
    ATTR_lamda_pwm_sub1,
    ATTR_language,
    ATTR_number_buffers_sub1,
    ATTR_number_obw_cwu_sub1,
    ATTR_number_obw_heating_curcuit_sub1,
    ATTR_oxygen_content_exhaust_sub1,
    ATTR_power_output_boiler_sub1,
    ATTR_state_lamda_sub1,
    ATTR_status_solar_connected_sub1,
    ATTR_target_temp_obw1_sub1,
    ATTR_temp_boiler_obli_sub1,
    ATTR_temp_boiler_return_sub1,
    ATTR_temp_boiler_sub1,
    ATTR_temp_boiler_target_sub3,
    ATTR_temp_boiler_target_sub4,
    ATTR_temp_buffer_bottom_sub1,
    ATTR_temp_buffer_top_sub1,
    ATTR_temp_exhaust_boiler_sub1,
    ATTR_temp_heating_curcuit1_sub1,
    ATTR_temp_heating_curcuit2_sub1,
    ATTR_temp_heating_curcuit3_sub1,
    ATTR_temp_heating_curcuit4_sub1,
    ATTR_temp_lamda_sub1,
    ATTR_temp_outside_sub1,
    ATTR_total_energy,
)

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(ATTR_language): cv.string,
    }
)


async def setup(coordinator: CoordinatorEntity):
    _LOGGER.debug(f"Setting up sensors - Devices: {coordinator.data.keys()}")

    sensors = []
    # ToDo cleanup
    for device_id in list(coordinator.data.keys()):
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_consumption_fuel_total_current_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfMass.KILOGRAMS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_consumption_fuel_current_day,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfMass.KILOGRAMS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_boiler_return_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_heating_curcuit1_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_heating_curcuit2_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_heating_curcuit3_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_heating_curcuit4_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_power_output_boiler_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=PERCENTAGE,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_lamda_pwm_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=PERCENTAGE,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_lamda_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_boiler_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_boiler_obli_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_exhaust_boiler_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_oxygen_content_exhaust_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=PERCENTAGE,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_current_status_burner_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_fuel_fill_level_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_outside_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_energy_meter_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_target_temp_obw1_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_buffer_top_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_buffer_bottom_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_number_obw_heating_curcuit_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_number_obw_cwu_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_number_buffers_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_status_solar_connected_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_state_lamda_sub1,
                Device_Id=device_id,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_boiler_target_sub3,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_temp_boiler_target_sub4,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            )
        )
        sensors.append(
            EstymaSensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_current_status_burner_sub1_int,
                Device_Id=device_id,
                state_class=SensorStateClass.MEASUREMENT,
            )
        )

        sensors.append(
            EstymaEnergySensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_total_energy,
                deviceReferenceAttribute=ATTR_consumption_fuel_total_current_sub1,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
                state_class=SensorStateClass.TOTAL_INCREASING,
            )
        )
        sensors.append(
            EstymaEnergySensor(
                coordinator=coordinator,
                deviceAttribute=ATTR_daily_energy,
                deviceReferenceAttribute=ATTR_consumption_fuel_current_day,
                Device_Id=device_id,
                native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
                state_class=SensorStateClass.TOTAL,
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
) -> None:
    """Set up the sensor platform."""
    _estymaApi = EstymaApi(
        Email=config[CONF_EMAIL],
        Password=config[CONF_PASSWORD],
        scanInterval=0,
        language=config[ATTR_language],
    )

    async_add_entities(await setup(Api=_estymaApi), update_before_add=True)


class EstymaSensor(SensorEntity, CoordinatorEntity):
    def __init__(
        self,
        coordinator: CoordinatorEntity,
        deviceAttribute,
        Device_Id,
        native_unit_of_measurement=None,
        state_class=None,
    ) -> None:
        super().__init__(coordinator=coordinator)
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute
        self._attr_state_class = None

        self._icon = "mdi:eye"

        if native_unit_of_measurement is not None:
            self._attr_native_unit_of_measurement = native_unit_of_measurement

            match native_unit_of_measurement:
                case UnitOfTemperature.CELSIUS:
                    self._icon = "mdi:thermometer"
                case UnitOfMass.KILOGRAMS:
                    self._icon = "mdi:weight"

        if state_class is not None:
            self._attr_state_class = state_class

        self._state = self.coordinator.data[Device_Id][self._attributename]
        self._available = True

        self.attrs: Dict[str, Any] = {
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
    def icon(self):
        return self._icon

    @property
    def unique_id(self) -> str:
        return f"{self._name}"

    @property
    def state(self) -> Optional[str]:
        return self._state

    @property
    def state_class(self):
        return self._attr_state_class

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

    @callback
    def _handle_coordinator_update(self) -> None:
        _LOGGER.debug(
            f"EstymaSensor - {self._name} - {self.attrs[CONF_DEVICE_ID]} - {self.coordinator.data[self.attrs[CONF_DEVICE_ID]][self._attributename]}"
        )

        self._state = self.coordinator.data[self.attrs[CONF_DEVICE_ID]][
            self._attributename
        ]

        self.async_write_ha_state()


class EstymaEnergySensor(SensorEntity, CoordinatorEntity):
    def __init__(
        self,
        coordinator: CoordinatorEntity,
        deviceAttribute,
        deviceReferenceAttribute,
        Device_Id,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
    ) -> None:
        super().__init__(coordinator=coordinator)
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute
        self._deviceReferenceAttribute = deviceReferenceAttribute
        self._deviceReferenceSensor = (
            f"sensor.{DOMAIN}_{Device_Id}_{deviceReferenceAttribute}"
        )

        if native_unit_of_measurement is not None:
            self._attr_native_unit_of_measurement = native_unit_of_measurement
            self._attr_native_unit_of_measurement

        if (
            native_unit_of_measurement == UnitOfEnergy.KILO_WATT_HOUR
            or native_unit_of_measurement == UnitOfEnergy.MEGA_WATT_HOUR
            or native_unit_of_measurement == UnitOfEnergy.WATT_HOUR
        ):
            self._attr_device_class = SensorDeviceClass.ENERGY

        self._attr_state_class = state_class

        self._state = float(
            self.coordinator.data[Device_Id][self._deviceReferenceAttribute] * 4.8
        )
        self._available = True

        self.attrs: Dict[str, Any] = {
            CONF_DEVICE_ID: Device_Id,
            "deviceReferenceSensor": self._deviceReferenceSensor,
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
    def state(self) -> Optional[str]:
        return self._state

    @property
    def last_reset(self) -> datetime | None:
        return None

    @property
    def native_value(self):
        return self._attr_state

    @property
    def state_class(self):
        return self._attr_state_class

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

    @callback
    def _handle_coordinator_update(self) -> None:
        _LOGGER.debug(
            f"EstymaSensor - {self._name} - {self.attrs[CONF_DEVICE_ID]} - {self.coordinator.data[self.attrs[CONF_DEVICE_ID]][self._deviceReferenceAttribute]}"
        )

        self._state = float(
            self.coordinator.data[self.attrs[CONF_DEVICE_ID]][
                self._deviceReferenceAttribute
            ]
            * 4.8
        )

        self.async_write_ha_state()
