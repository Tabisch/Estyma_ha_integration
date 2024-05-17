import asyncio
import logging
from datetime import timedelta, datetime
import traceback
from typing import Any, Callable, Dict, Optional

from EstymaApiWrapper import EstymaApi

import voluptuous as vol

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass, PLATFORM_SCHEMA
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
    UnitOfTemperature,
    UnitOfMass,
    UnitOfEnergy
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

    sensors = []
    #ToDo cleanup
    for device_id in list(Api.devices.keys()):
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_consumption_fuel_total_current_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfMass.KILOGRAMS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_consumption_fuel_current_day, Device_Id=device_id, native_unit_of_measurement=UnitOfMass.KILOGRAMS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_boiler_return_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_heating_curcuit1_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_heating_curcuit2_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_heating_curcuit3_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_heating_curcuit4_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_power_output_boiler_sub1, Device_Id=device_id, native_unit_of_measurement=PERCENTAGE, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_lamda_pwm_sub1, Device_Id=device_id, native_unit_of_measurement=PERCENTAGE, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_lamda_sub1, Device_Id=device_id))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_boiler_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_boiler_obli_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_exhaust_boiler_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_oxygen_content_exhaust_sub1, Device_Id=device_id, native_unit_of_measurement=PERCENTAGE, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_current_status_burner_sub1, Device_Id=device_id))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_fuel_fill_level_sub1, Device_Id=device_id))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_outside_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_energy_meter_sub1, Device_Id=device_id))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_obw1_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_buffer_top_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_buffer_bottom_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_number_obw_heating_curcuit_sub1, Device_Id=device_id))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_number_obw_cwu_sub1, Device_Id=device_id))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_number_buffers_sub1, Device_Id=device_id))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_status_solar_connected_sub1, Device_Id=device_id))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_state_lamda_sub1, Device_Id=device_id))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_boiler_target_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_boiler_target_sub3, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_temp_boiler_target_sub4, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_operation_mode_boiler_sub1, Device_Id=device_id))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_room_comf_heating_curcuit_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_room_comf_heating_curcuit_sub3, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_room_comf_heating_curcuit_sub4, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_room_eco_heating_curcuit_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_room_eco_heating_curcuit_sub3, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_room_eco_heating_curcuit_sub4, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_buffer_top_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_buffer_top_sub3, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_buffer_top_sub4, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_buffer_bottom_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_buffer_bottom_sub3, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_target_temp_buffer_bottom_sub4, Device_Id=device_id, native_unit_of_measurement=UnitOfTemperature.CELSIUS))
        sensors.append(EstymaSensor(estymaapi=Api, deviceAttribute=ATTR_current_status_burner_sub1_int, Device_Id=device_id, state_class=SensorStateClass.MEASUREMENT))

        sensors.append(EstymaEnergySensor(Api, ATTR_total_energy, ATTR_consumption_fuel_total_current_sub1, Device_Id=device_id, native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR, state_class=SensorStateClass.TOTAL_INCREASING))
        sensors.append(EstymaEnergySensor(Api, ATTR_daily_energy, ATTR_consumption_fuel_current_day, Device_Id=device_id, native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR, state_class=SensorStateClass.TOTAL))

    return sensors

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    config = hass.data[DOMAIN][entry.entry_id]

    _estymaApi = EstymaApi(Email= config[CONF_EMAIL], Password= config[CONF_PASSWORD], scanInterval= 0, language= config[ATTR_language])
    
    async_add_entities(await setup(Api= _estymaApi), update_before_add=True)

async def async_setup_platform(hass: HomeAssistantType, config: ConfigType, async_add_entities: Callable, discovery_info: Optional[DiscoveryInfoType] = None,) -> None:
    """Set up the sensor platform."""
    _estymaApi = EstymaApi(Email= config[CONF_EMAIL], Password= config[CONF_PASSWORD], scanInterval= 0, language= config[ATTR_language])
    
    async_add_entities(await setup(Api= _estymaApi), update_before_add=True)

class EstymaSensor(SensorEntity):

    def __init__(self, estymaapi: EstymaApi, deviceAttribute, Device_Id, native_unit_of_measurement = None, state_class = None) -> None:
        super().__init__()
        self._estymaapi = estymaapi
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute
        
        if(native_unit_of_measurement != None):
            self._attr_native_unit_of_measurement = native_unit_of_measurement

            match native_unit_of_measurement:
                case UnitOfTemperature.CELSIUS: 
                    self._icon = "mdi:thermometer"
                case UnitOfMass.KILOGRAMS:
                    self._icon = "mdi:weight"
                case _:
                    self._icon = "mdi:eye"

        if(state_class != None):
            self._attr_state_class = state_class

        self._state = None
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

    async def async_update(self):
        _LOGGER.debug(f"updating {self._name} - {self.attrs[CONF_DEVICE_ID]}")

        #while(self._estymaapi.updatingData == True):
        #    _LOGGER.debug(f"waiting for update to finish {self._name} - {self.attrs[CONF_DEVICE_ID]}")
        #    asyncio.sleep(1)

        try:
            data = await self._estymaapi.getDeviceData(self.attrs[CONF_DEVICE_ID])

            self._state = data[self._attributename]
        except:
            _LOGGER.exception(traceback.print_exc())

class EstymaEnergySensor(SensorEntity):

    def __init__(self, estymaapi: EstymaApi, deviceAttribute, deviceReferenceAttribute, Device_Id,  native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR, state_class = SensorStateClass.TOTAL) -> None:
        super().__init__()
        self._estymaapi = estymaapi
        self._name = f"{DOMAIN}_{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute
        self._deviceReferenceAttribute = f"sensor.{DOMAIN}_{Device_Id}_{deviceReferenceAttribute}"
        
        if(native_unit_of_measurement != None):
            self._attr_native_unit_of_measurement = native_unit_of_measurement
            self._attr_native_unit_of_measurement

        if(native_unit_of_measurement == UnitOfEnergy.KILO_WATT_HOUR or native_unit_of_measurement == UnitOfEnergy.MEGA_WATT_HOUR or native_unit_of_measurement == UnitOfEnergy.WATT_HOUR) :
            self._attr_device_class = SensorDeviceClass.ENERGY

        self._attr_state_class = state_class

        self._state = None
        self._available = True

        self.attrs: Dict[str, Any] = {
            CONF_DEVICE_ID: Device_Id,
            "deviceReferenceAttribute": self._deviceReferenceAttribute
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

    async def async_update(self):
        _deviceReferenceAttributeValue = self.hass.states.get(self._deviceReferenceAttribute)
        _LOGGER.debug(f"{self._name} - {self._deviceReferenceAttribute}")

        if _deviceReferenceAttributeValue:
            _LOGGER.debug(f"{self._name} - {self._deviceReferenceAttribute} - {_deviceReferenceAttributeValue.state}")
            self._state = float(_deviceReferenceAttributeValue.state) * 4.8