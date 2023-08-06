from antidote import inject, Provide

from AsteriskRealtimeData.application.queue_status_repository import (
    QueueStatusRepository,
)
from AsteriskRealtimeData.domain.queue_status.queue_status import QueueStatus
from AsteriskRealtimeData.domain.queue_status.queue_status_vo import QueueStatusVo


class QueueStatusService:
    @inject
    def create_queue_status(
        self, queue_status_vo: QueueStatusVo, repository: Provide[QueueStatusRepository]
    ) -> QueueStatusVo:

        repository.save(queue_status_vo, {"status_code": queue_status_vo.status_code})

        return QueueStatusVo(
            status_code=queue_status_vo.status_code,
            description=queue_status_vo.description,
        )

    @inject()
    def list_queue_status(
        self, repository: Provide[QueueStatusRepository]
    ) -> list[QueueStatusVo]:
        result: list = []
        for document in repository.list():
            result.append(
                QueueStatusVo(
                    status_code=document["status_code"],
                    description=document["description"],
                )
            )
        return result

    @inject
    def get_queue_status(
        self, status_code: str, repository: Provide[QueueStatusRepository]
    ) -> QueueStatusVo:
        queue_status = repository.get_by_criteria({"status_code": status_code})
        return QueueStatusVo(
            status_code=queue_status["status_code"],
            description=queue_status["description"],
        )

    @inject
    def delete_queue_status(
        self, status_code: str, repository: Provide[QueueStatusRepository]
    ) -> QueueStatusVo:
        repository.delete_by_criteria({"status_code": status_code})
        return QueueStatusVo(status_code=status_code, description="")
