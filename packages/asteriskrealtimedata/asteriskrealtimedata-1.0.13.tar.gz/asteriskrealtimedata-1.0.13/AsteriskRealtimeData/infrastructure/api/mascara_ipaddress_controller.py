from AsteriskRealtimeData.application.mascara_ipaddress_service import (
    MascaraIpaddressService,
)
from AsteriskRealtimeData.domain.mascara_ipaddress.mascara_ipaddress_vo import (
    MascaraIpaddressVo,
)


class MascaraIpaddressController:
    def create(self, mascara_ipaddress_vo: MascaraIpaddressVo) -> MascaraIpaddressVo:
        return MascaraIpaddressService().create_mascara_ipaddress(mascara_ipaddress_vo)

    def list(self) -> list[dict]:
        mascara_ipaddresses = MascaraIpaddressService().list_mascara_ipaddress()
        result: list = []

        for mascara_ipaddress in mascara_ipaddresses:
            result.append(mascara_ipaddress.as_dict())

        return result

    def get_by_ipaddress(self, ipaddress: str) -> dict:
        return MascaraIpaddressService().get_mascara_ipaddress(ipaddress).as_dict()

    def delete_by_ipaddress(self, ipaddress: str) -> dict:
        return MascaraIpaddressService().delete_mascara_ipaddress(ipaddress)
