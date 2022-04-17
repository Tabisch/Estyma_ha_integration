import logging
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.entity_registry import (
    async_entries_for_config_entry,
    async_get_registry,
)

from const import DOMAIN

_LOGGER = logging.getLogger(__name__)

data_schema = {
    vol.Required("email"): str,
    vol.Required("password"): str,
}

class IgneoFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Igneo config flow."""

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Handle user step."""

        errors: Dict[str, str] = {}

        if user_input is not None:
            #ToDo implement login validation
            try:
                # await validate_auth(user_input[CONF_ACCESS_TOKEN], self.hass)
                raise ValueError
            except ValueError:
                errors["base"] = "auth"

            if not errors:
                return self.async_create_entry(title="Igneo", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )