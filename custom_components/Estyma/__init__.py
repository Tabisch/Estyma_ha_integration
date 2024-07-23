import asyncio
import logging
from homeassistant import config_entries, core
from .const import DOMAIN, ATTR_language
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import Platform
from .coordinator import EstymaCoordinator

from EstymaApiWrapper import EstymaApi

from homeassistant.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
)

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SWITCH, Platform.SELECT]

_LOGGER = logging.getLogger(__name__)
_failedInitSleepTime = 5

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(ATTR_language): cv.string,
    }
)


async def async_setup(hass, config):
    """Set up the Estyma integration."""
    _LOGGER.debug("Estyma")
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    config = hass.data[DOMAIN][entry.entry_id]

    _estymaApi = EstymaApi(
        Email=config[CONF_EMAIL],
        Password=config[CONF_PASSWORD],
        scanInterval=0,
        language=config[ATTR_language],
    )

    while _estymaApi.initialized is False:
        await _estymaApi.initialize(throw_Execetion=False)
        if _estymaApi.initialized is False:
            break
        else:
            await asyncio.sleep(_failedInitSleepTime)

    coordinator = EstymaCoordinator(hass, estymaApi=_estymaApi)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry=entry, platforms=PLATFORMS
    )

    return True
