from AsteriskRealtimeData.domain import pause_reason
from AsteriskRealtimeData.application.mascara_ipaddress_repository import (
    MascaraIpaddressRepository,
)
from antidote import inject, Provide
from AsteriskRealtimeData.domain.mascara_ipaddress.mascara_ipaddress import (
    MascaraIpaddress,
)
from AsteriskRealtimeData.domain.mascara_ipaddress.mascara_ipaddress_vo import (
    MascaraIpaddressVo,
)


class MascaraIpaddressService:
    @inject
    def create_mascara_ipaddress(
        self,
        mascara_ipaddress_vo: MascaraIpaddressVo,
        repository: Provide[MascaraIpaddressRepository],
    ) -> MascaraIpaddressVo:

        mascara_ipaddress = MascaraIpaddress(ip_address=mascara_ipaddress_vo.ipaddress)

        repository.save(
            mascara_ipaddress, {"ipaddress": mascara_ipaddress_vo.ipaddress}
        )

        return MascaraIpaddressVo(ipaddress=mascara_ipaddress_vo.ipaddress)

    @inject()
    def list_mascara_ipaddress(
        self, repository: Provide[MascaraIpaddressRepository]
    ) -> list[MascaraIpaddressVo]:
        result: list = []
        for document in repository.list():
            result.append(MascaraIpaddressVo(ipaddress=document["ipaddress"]))
        return result

    @inject
    def get_mascara_ipaddress(
        self, ipaddress: str, repository: Provide[MascaraIpaddressRepository]
    ) -> MascaraIpaddressVo:
        mascara_ipaddress = repository.get_by_criteria({"ipaddress": ipaddress})
        return MascaraIpaddressVo(ipaddress=mascara_ipaddress["ipaddress"])

    @inject
    def delete_mascara_ipaddress(
        self, ipaddress: str, repository: Provide[MascaraIpaddressRepository]
    ) -> MascaraIpaddressVo:
        repository.delete_by_criteria({"ipaddress": ipaddress})
        return MascaraIpaddressVo(ipaddress=ipaddress)
