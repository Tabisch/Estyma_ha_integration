from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

def setup(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    hass.data.setdefault(DOMAIN, {})

    hass.states.set("igneo.world", "Paulus")

    return True