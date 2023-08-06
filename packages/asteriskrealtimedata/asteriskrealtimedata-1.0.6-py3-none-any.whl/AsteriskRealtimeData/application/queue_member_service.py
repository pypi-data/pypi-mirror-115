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
            ipaddress=queue_member_vo.ipaddress,
            membername=queue_member_vo.membername,
            last_status_datetime=queue_member_vo.last_status_datetime,
            is_queuemember=is_queue_member,
        )

        repository.save(queue_member, {"ipaddress": queue_member_vo.ipaddress})

        return QueueMemberVo(
            peer=queue_member_vo.peer,
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
                    pause_code=document["pause_code"],
                    description=document["description"],
                )
            )
        return result

    @inject
    def get_queue_member(
        self, pause_code: str, repository: Provide[QueueMemberRepository]
    ) -> QueueMemberVo:
        queue_member = repository.get_by_criteria({"pause_code": pause_code})
        return QueueMemberVo(
            pause_code=queue_member["pause_code"],
            description=queue_member["description"],
        )

    @inject
    def delete_queue_member(
        self, pause_code: str, repository: Provide[QueueMemberRepository]
    ) -> QueueMemberVo:
        repository.delete_by_criteria({"pause_code": pause_code})
        return QueueMemberVo(pause_code=pause_code, description="")
