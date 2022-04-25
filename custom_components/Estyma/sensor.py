import logging
from datetime import timedelta
import traceback
from typing import Any, Callable, Dict, Optional

from EstymaApiWrapper import EstymaApi

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.sensor import SensorEntity
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
    PERCENTAGE,
    TEMP_CELSIUS,
    MASS_KILOGRAMS
)

from .const import *

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(ATTR_language): cv.string
    }
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    _LOGGER.info("Estyma entry")
    config = hass.data[DOMAIN][entry.entry_id]

    Api = EstymaApi(Email= config[CONF_EMAIL], Password= config[CONF_PASSWORD], language= config[ATTR_language])
    
    await Api.initialize()

    sensors = []
    #ToDo cleanup
    for device_id in list(Api.devices.keys()):
        sensors.append(EstymaSensor(Api, ATTR_consumption_fuel_total_current_sub1, device_id, MASS_KILOGRAMS))
        sensors.append(EstymaSensor(Api, ATTR_consumption_fuel_current_day, device_id, MASS_KILOGRAMS))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_return_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_heating_curcuit1_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_heating_curcuit2_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_heating_curcuit3_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_heating_curcuit4_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_power_output_boiler_sub1, device_id, MASS_KILOGRAMS))
        sensors.append(EstymaSensor(Api, ATTR_lamda_pwm_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_temp_lamda_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_obli_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_exhaust_boiler_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_oxygen_content_exhaust_sub1, device_id, PERCENTAGE))
        sensors.append(EstymaSensor(Api, ATTR_status_burner_current_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_fuel_fill_level_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_temp_outside_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_energy_meter_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_status_boiler_pump_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_obw1_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_status_pump_heating_curcuit1_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_buffer_top_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_buffer_bottom_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_number_obw_heating_curcuit_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_number_obw_cwu_sub1, device_id))
    #   sensors.append(EstymaSensor(Api, ATTR_number_buffers_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_status_solar_connected_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_state_lamda_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_target_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_target_sub3, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_target_sub4, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_burner_enabled_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_operation_mode_boiler_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_status_controller_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_room_comf_heating_curcuit_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_room_comf_heating_curcuit_sub3, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_room_comf_heating_curcuit_sub4, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_room_eco_heating_curcuit_sub1, device_id, TEMP_CELSIUS))
    #   sensors.append(EstymaSensor(Api, ATTR_target_temp_room_eco_heating_curcuit_sub3, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_room_eco_heating_curcuit_sub4, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_top_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_top_sub3, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_top_sub4, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_bottom_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_bottom_sub3, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_bottom_sub4, device_id, TEMP_CELSIUS))
    #    sensors.append(EstymaSensor(Api, ATTR_current_status_burner_sub1_int, device_id))
    
    async_add_entities(sensors, update_before_add=True)

async def async_setup_platform(hass: HomeAssistantType, config: ConfigType, async_add_entities: Callable, discovery_info: Optional[DiscoveryInfoType] = None,) -> None:
    """Set up the sensor platform."""
    Api = EstymaApi(Email= config[CONF_EMAIL], Password= config[CONF_PASSWORD], language= config[ATTR_language])
    
    await Api.initialize()

    sensors = []
    #ToDo cleanup
    for device_id in list(Api.devices.keys()):
        sensors.append(EstymaSensor(Api, ATTR_consumption_fuel_total_current_sub1, device_id, MASS_KILOGRAMS))
        sensors.append(EstymaSensor(Api, ATTR_consumption_fuel_current_day, device_id, MASS_KILOGRAMS))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_return_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_heating_curcuit1_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_heating_curcuit2_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_heating_curcuit3_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_heating_curcuit4_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_power_output_boiler_sub1, device_id, MASS_KILOGRAMS))
        sensors.append(EstymaSensor(Api, ATTR_lamda_pwm_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_temp_lamda_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_obli_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_exhaust_boiler_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_oxygen_content_exhaust_sub1, device_id, PERCENTAGE))
        sensors.append(EstymaSensor(Api, ATTR_status_burner_current_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_fuel_fill_level_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_temp_outside_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_energy_meter_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_status_boiler_pump_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_obw1_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_status_pump_heating_curcuit1_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_buffer_top_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_buffer_bottom_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_number_obw_heating_curcuit_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_number_obw_cwu_sub1, device_id))
    #   sensors.append(EstymaSensor(Api, ATTR_number_buffers_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_status_solar_connected_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_state_lamda_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_target_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_target_sub3, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_temp_boiler_target_sub4, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_burner_enabled_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_operation_mode_boiler_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_status_controller_sub1, device_id))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_room_comf_heating_curcuit_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_room_comf_heating_curcuit_sub3, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_room_comf_heating_curcuit_sub4, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_room_eco_heating_curcuit_sub1, device_id, TEMP_CELSIUS))
    #    sensors.append(EstymaSensor(Api, ATTR_target_temp_room_eco_heating_curcuit_sub3, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_room_eco_heating_curcuit_sub4, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_top_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_top_sub3, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_top_sub4, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_bottom_sub1, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_bottom_sub3, device_id, TEMP_CELSIUS))
        sensors.append(EstymaSensor(Api, ATTR_target_temp_buffer_bottom_sub4, device_id, TEMP_CELSIUS))
    #    sensors.append(EstymaSensor(Api, ATTR_current_status_burner_sub1_int, device_id))
    
    async_add_entities(sensors, update_before_add=True)

class EstymaSensor(SensorEntity):

    def __init__(self, estymaapi: EstymaApi, deviceAttribute, Device_Id, native_unit_of_measurement = None) -> None:
        super().__init__()
        self._estymaapi = estymaapi
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute
        
        if(native_unit_of_measurement != None):
            self._attr_native_unit_of_measurement = native_unit_of_measurement

        self._state = None
        self._available = True
        self.attrs: Dict[str, Any] = {CONF_DEVICE_ID: Device_Id}

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
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    @property
    def state(self) -> Optional[str]:
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
        if(self._estymaapi.initialized == False):
            _LOGGER.info("Estyma api not initialized")
            _LOGGER.info(f'Estyma api return code {self._estymaapi.returncode}')
            return

        try:
            _LOGGER.info(f"updating {self._name} - {self.attrs[CONF_DEVICE_ID]}")
            data = await self._estymaapi.getDeviceData(self.attrs[CONF_DEVICE_ID])
            self._state = data[self._attributename]
        except:
            _LOGGER.exception(traceback.print_exc())