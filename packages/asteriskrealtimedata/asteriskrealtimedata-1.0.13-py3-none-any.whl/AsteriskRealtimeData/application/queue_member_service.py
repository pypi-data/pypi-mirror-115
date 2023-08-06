from AsteriskRealtimeData.application.queue_member_repository import (
    QueueMemberRepository,
)
from antidote import inject, Provide
from AsteriskRealtimeData.domain.queue_member.queue_member import QueueMember
from AsteriskRealtimeData.domain.queue_member.queue_member_vo import QueueMemberVo
from AsteriskRealtimeData.application.mascara_ipaddress_service import (
    MascaraIpaddressService,
)


class QueueMemberService:
    @inject
    def create_queue_member(
        self, queue_member_vo: QueueMemberVo, repository: Provide[QueueMemberRepository]
    ) -> QueueMemberVo:

        mascara_ipaddress = MascaraIpaddressService().get_mascara_ipaddress(
            queue_member_vo.ipaddress
        )

        is_queue_member = mascara_ipaddress.ipaddress

        queue_member = QueueMember(
            peer=queue_member_vo.peer,
            actual_status=queue_member_vo.actual_status,
            ipaddress=queue_member_vo.ipaddress,
            membername=queue_member_vo.membername,
            last_status_datetime=queue_member_vo.last_status_datetime,
            is_queuemember=is_queue_member,
        )

        repository.save(queue_member, {"ipaddress": queue_member_vo.ipaddress})

        return QueueMemberVo(
            peer=queue_member_vo.peer,
            actual_status=queue_member_vo.actual_status,
            ipaddress=queue_member_vo.ipaddress,
            membername=queue_member_vo.membername,
            last_status_datetime=queue_member_vo.last_status_datetime,
            is_queuemember=is_queue_member,
        )

    @inject()
    def list_queue_member(
        self, repository: Provide[QueueMemberRepository]
    ) -> list[QueueMemberVo]:
        result: list = []
        for document in repository.list():
            result.append(
                QueueMemberVo(
                    peer=document["peer"],
                    actual_status=document["actual_status"],
                    ipaddress=document["ipaddress"],
                    membername=document["membername"],
                    last_status_datetime=document["last_status_datetime"],
                    is_queuemember=document["is_queuemember"],
                )
            )
        return result

    @inject
    def get_queue_member(
        self, peer: str, repository: Provide[QueueMemberRepository]
    ) -> QueueMemberVo:
        queue_member = repository.get_by_criteria({"peer": peer})
        return QueueMemberVo(
            peer=queue_member["peer"],
            actual_status=queue_member["actual_status"],
            ipaddress=queue_member["ipaddress"],
            membername=queue_member["membername"],
            last_status_datetime=queue_member["last_status_datetime"],
            is_queuemember=queue_member["is_queuemember"],
        )

    @inject
    def delete_queue_member(
        self, peer: str, repository: Provide[QueueMemberRepository]
    ) -> QueueMemberVo:
        repository.delete_by_criteria({"peer": peer})
        return QueueMemberVo(
            peer=peer,
            actual_status="",
            ipaddress="",
            membername="",
            last_status_datetime="",
            is_queuemember="",
        )
