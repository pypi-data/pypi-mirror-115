from AsteriskRealtimeData.application.queue_status_service import QueueStatusService
from AsteriskRealtimeData.domain.queue_status.queue_status_vo import QueueStatusVo


class QueueStatusController:
    def create(self, queue_status_vo: QueueStatusVo) -> QueueStatusVo:
        return QueueStatusService().create_queue_status(queue_status_vo)

    def list(self) -> list[dict]:
        queues_status = QueueStatusService().list_queue_status()
        result: list = []

        for queue_status in queues_status:
            result.append(queue_status.as_dict())

        return result

    def get_by_status_code(self, status_code: str) -> dict:
        return QueueStatusService().get_queue_status(status_code).as_dict()

    def delete_by_status_code(self, status_code: str) -> dict:
        return QueueStatusService().delete_queue_status(status_code)
