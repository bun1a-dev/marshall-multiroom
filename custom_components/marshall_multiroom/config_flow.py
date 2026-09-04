"""Config flow for Marshall Multi-Room."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_PIN, DEFAULT_PIN, DOMAIN, NODE_FRIENDLY_NAME, NODE_VERSION
from .fsapi_client import FsApiClient, FsApiError

_LOGGER = logging.getLogger(__name__)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PIN, default=DEFAULT_PIN): str,
    }
)


class MarshallMultiroomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Marshall Multi-Room speakers."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            pin = user_input[CONF_PIN]

            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()

            session: aiohttp.ClientSession = async_get_clientsession(self.hass)
            client = FsApiClient(host, pin, session)

            try:
                version = await client.get(NODE_VERSION)
                try:
                    friendly_name = await client.get(NODE_FRIENDLY_NAME)
                except FsApiError:
                    friendly_name = host
            except (FsApiError, aiohttp.ClientError, TimeoutError):
                errors["base"] = "cannot_connect"
            else:
                _LOGGER.debug("Connected to Marshall speaker, firmware=%s", version)
                return self.async_create_entry(
                    title=friendly_name or host,
                    data={CONF_HOST: host, CONF_PIN: pin, CONF_NAME: friendly_name or host},
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_SCHEMA, errors=errors
        )
