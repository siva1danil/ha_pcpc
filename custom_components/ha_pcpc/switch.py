import asyncio
import logging

from wakeonlan import send_magic_packet
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from datetime import timedelta

from .const import DOMAIN
from .model import PCPCModel

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=10)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = entry.data
    model = PCPCModel.from_config(data)
    entity = PCPCSwitch(model)
    async_add_entities([entity], True)

class PCPCSwitch(SwitchEntity):
    def __init__(self, model: PCPCModel):
        self._model = model
        self._is_on = False

        self._attr_unique_id = model.uuid
        self._attr_name = model.name
        self._attr_should_poll = True
        self._attr_extra_state_attributes = { "mac": self._model.mac, "ip": self._model.ip }

    @property
    def device_info(self) -> DeviceInfo:
        details = []
        if self._model.mac:
            details.append(self._model.mac)
        if self._model.ip:
            details.append(self._model.ip)
        
        return DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=self._model.name,
            manufacturer="PC Power Control",
            model=" / ".join(details),
        )

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_update(self):
        if not self._model.ip:
            self._is_on = False
            return

        cmd = f"ping -c 1 -W 1 {self._model.ip}"
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        await proc.communicate()
        self._is_on = proc.returncode == 0

    async def async_turn_on(self, **kwargs):
        if not self._model.mac:
            return

        try:
            send_magic_packet(self._model.mac)
        except Exception as e:
            _LOGGER.error("Failed to send WoL packet to %s: %s", self._model.mac, e)

    async def async_turn_off(self, **kwargs):
        _LOGGER.warning("Turn off not supported for %s", self._model.name)
