from AsteriskRealtimeData.application.mascara_ipaddress_service import (
    MascaraIpaddressService,
)
from AsteriskRealtimeData.domain.mascara_ipaddress.mascara_ipaddress_vo import (
    MascaraIpaddressVo,
)


class MascaraIpaddressController:
    def create(self, mascara_ipaddress: MascaraIpaddressVo) -> MascaraIpaddressVo:
        mascara_ipaddress_parameter = MascaraIpaddressVo(**mascara_ipaddress)
        return MascaraIpaddressService().create_mascara_ipaddress(
            mascara_ipaddress_parameter
        )

    def list(self) -> list[dict]:
        mascara_ipaddresses = MascaraIpaddressService().list_mascara_ipaddress()
        result: list = []

        for mascara_ipaddress in mascara_ipaddresses:
            result.append(mascara_ipaddress.as_dict())

        return result

    def get_by_criteria(self, search_criteria: str) -> dict:
        return (
            MascaraIpaddressService().get_mascara_ipaddress(search_criteria).as_dict()
        )

    def delete_by_criteria(self, search_criteria: str) -> dict:
        return MascaraIpaddressService().delete_mascara_ipaddress(search_criteria)
