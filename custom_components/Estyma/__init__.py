import logging

from homeassistant import config_entries, core



from .const import DOMAIN

PLATFORMS = ["sensor","binary_sensor"]


_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the Estyma integration."""
    _LOGGER.debug("Estyma")
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "binary_sensor")
    )

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True
