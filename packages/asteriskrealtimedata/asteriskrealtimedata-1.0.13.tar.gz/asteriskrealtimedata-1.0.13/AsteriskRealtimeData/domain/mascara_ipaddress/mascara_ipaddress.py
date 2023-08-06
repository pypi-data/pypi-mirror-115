from AsteriskRealtimeData.domain.entity import Entity
from dataclasses import dataclass


@dataclass
class MascaraIpaddress(Entity):
    ip_address: str = "0.0.0.0"

    def __init__(self, ip_address):
        self.ip_address = ip_address

    def get_ip_address(self) -> str:
        return self.ip_address

    def as_dict(self):
        return self.__repr__()

    def __repr__(self):
        return {"id": self.get_id(), "ipaddress": self.get_ip_address()}
