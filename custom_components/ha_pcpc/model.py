import ipaddress
import re

from dataclasses import dataclass
from typing import Optional

from .const import CONF_UUID, CONF_NAME, CONF_MAC, CONF_IP, DEFAULT_NAME

@dataclass(frozen=True)
class PCPCModel:
    uuid: str
    name: str
    mac: Optional[str]
    ip: Optional[str]

    @staticmethod
    def from_config(config: dict) -> "PCPCModel":
        uuid = config.get(CONF_UUID, "")
        name = config.get(CONF_NAME, DEFAULT_NAME)
        mac = config.get(CONF_MAC)
        ip = config.get(CONF_IP)

        if not PCPCModel.validate_mac(mac):
            raise ValueError(f"invalid_mac")
        if not PCPCModel.validate_ip(ip):
            raise ValueError(f"invalid_ip")

        if mac is None and ip is None:
            raise ValueError("empty_config")

        return PCPCModel(
            uuid=uuid,
            name=name,
            mac=mac,
            ip=ip,
        )

    @staticmethod
    def validate_ip(ip: str | None) -> bool:
        if ip is None:
            return True
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_mac(mac: str | None) -> bool:
        if mac is None:
            return True
        return re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac) is not None