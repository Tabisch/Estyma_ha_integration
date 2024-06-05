import logging
from homeassistant import config_entries, core
from .const import DOMAIN, ATTR_language
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA

from homeassistant.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
)

PLATFORMS = ["sensor", "binary_sensor", "switch"]

_LOGGER = logging.getLogger(__name__)

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

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "binary_sensor")
    )

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )

    return True
