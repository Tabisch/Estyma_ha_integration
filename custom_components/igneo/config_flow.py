import logging
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_EMAIL,
    CONF_PASSWORD
    
)
from homeassistant.helpers.entity_registry import (
    async_entries_for_config_entry,
    async_get_registry,
)

from EstymaApiWrapper import EstymaApi

from const import DOMAIN

_LOGGER = logging.getLogger(__name__)

options_schema = vol.Schema(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string
    }
)

class IgneoFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Igneo config flow."""

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Handle user step."""

        errors: Dict[str, str] = {}

        if user_input is not None:
            #ToDo implement login validation
            try:
                # await validate_auth(user_input[CONF_ACCESS_TOKEN], self.hass)
                (EstymaApi(Email= CONF_EMAIL, Password= CONF_PASSWORD)).login()
            except ValueError:
                errors["base"] = "auth"

            if not errors:
                return self.async_create_entry(title="Igneo", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=options_schema, errors=errors
        )