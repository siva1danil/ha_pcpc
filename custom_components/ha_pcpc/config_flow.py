import voluptuous as vol
import uuid

from homeassistant import config_entries

from .const import DOMAIN, VERSION, CONF_UUID, CONF_NAME, CONF_MAC, CONF_IP, DEFAULT_NAME
from .model import PCPCModel

class PCPCConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = VERSION

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                user_input[CONF_UUID] = str(uuid.uuid4())
                for key in (CONF_MAC, CONF_IP):
                    value = user_input.get(key, "").strip()
                    user_input[key] = value if value else None
                PCPCModel.from_config(user_input)
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data=user_input,
                )
            except ValueError as e:
                errors["base"] = str(e)

        schema = vol.Schema({
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Optional(CONF_MAC, default=""): str,
            vol.Optional(CONF_IP, default=""): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )
