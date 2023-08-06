from dataclasses import dataclass


@dataclass
class MascaraIpaddressVo:
    ipaddress: str

    def as_dict(self):
        return {"ipaddress": self.ipaddress}
