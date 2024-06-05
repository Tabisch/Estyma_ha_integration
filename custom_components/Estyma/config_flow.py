import logging
from typing import Any, Optional

from EstymaApiWrapper import EstymaApi
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

from .const import DOMAIN, ATTR_language

_LOGGER = logging.getLogger(__name__)

options_schema = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(ATTR_language): str,
    }
)


class EstymaFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Estyma config flow."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input: Optional[dict[str, Any]] = None):
        """Handle user step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            # ToDo implement login validation
            try:
                # await validate_auth(user_input[CONF_ACCESS_TOKEN], self.hass)
                await (
                    EstymaApi(
                        Email=user_input[CONF_EMAIL], Password=user_input[CONF_PASSWORD]
                    )
                )._login()
            except ValueError:
                errors["base"] = "auth"

            if not errors:
                return self.async_create_entry(title="Estyma", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=options_schema, errors=errors
        )
