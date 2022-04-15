import logging

from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

PLATFORMS = ["sensor"]


_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the Igneo integration."""
    _LOGGER.debug("igneo")
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Igneo from a config entry."""
    _LOGGER.debug("Igneo async_setup_entry")

    hass.data[DOMAIN][entry.entry_id] = {}

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True