"""Hisense TV config flow."""
from ast import IsNot
import json
from json.decoder import JSONDecodeError
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class IgneoFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Igneo config flow."""

    def __init__(self):
        """Initialize the config flow."""
        self._mac = None
        self._name = None
        self._mqtt_in = None
        self._mqtt_out = None
        self._unsubscribe_auth = None
        self._unsubscribe_sourcelist = None

    async def async_step_user(self, user_input=None):
        """Handle user step."""

        if user_input is not None:
            #ToDo implement login validation
            valid = True

            if valid is True:
                return self.async_create_entry()
        data_schema = {
            vol.Required("email"): str,
            vol.Required("password"): str,
        }

        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(data_schema)
        )