from AsteriskRealtimeData.application.queue_status_service import QueueStatusService
from AsteriskRealtimeData.domain.queue_status.queue_status_vo import QueueStatusVo


class QueueStatusController:
    def create(self, queue_status: QueueStatusVo) -> QueueStatusVo:
        queue_status_parameter = QueueStatusVo(**queue_status)
        return QueueStatusService().create_queue_status(queue_status_parameter)

    def list(self) -> list[dict]:
        queues_status = QueueStatusService().list_queue_status()
        result: list = []

        for queue_status in queues_status:
            result.append(queue_status.as_dict())

        return result

    def get_by_criteria(self, search_criteria: str) -> dict:
        return QueueStatusService().get_queue_status(search_criteria).as_dict()

    def delete_by_criteria(self, search_criteria: str) -> dict:
        return QueueStatusService().delete_queue_status(search_criteria)
