from AsteriskRealtimeData.application.queue_member_service import QueueMemberService
from AsteriskRealtimeData.domain.queue_member.queue_member_vo import QueueMemberVo


class QueueMemberController:
    def create(self, queue_member_vo: QueueMemberVo) -> QueueMemberVo:
        return QueueMemberService().create_queue_member(queue_member_vo)

    def list(self) -> list[dict]:
        queue_members = QueueMemberService().list_queue_member()
        result: list = []

        for queue_member in queue_members:
            result.append(queue_member.as_dict())

        return result

    def get_by_peer(self, peer: str) -> dict:
        return QueueMemberService().get_queue_member(peer).as_dict()

    def delete_by_peer(self, peer: str) -> dict:
        return QueueMemberService().delete_queue_member(peer)
