from antidote import Provide, inject
from AsteriskRealtimeData.application.pause_reason_repository import (
    PauseReasonRepository,
)
from AsteriskRealtimeData.domain.pause_reason.pause_reason import PauseReason
from AsteriskRealtimeData.domain.pause_reason.pause_reason_created_vo import (
    PauseReasonCreatedVo,
)
from AsteriskRealtimeData.domain.pause_reason.pause_reasons_vo import PauseReasonVo


class PauseReasonService:
    @inject
    def create_pause_reason(
        self, pause_reason_vo: PauseReasonVo, repository: Provide[PauseReasonRepository]
    ) -> PauseReasonCreatedVo:

        pause_reason = PauseReason(
            pause_code=pause_reason_vo.pause_code,
            description=pause_reason_vo.description,
        )

        repository.save(pause_reason, {"pause_code": pause_reason_vo.pause_code})

        return PauseReasonCreatedVo(
            pause_code=pause_reason_vo.pause_code,
            description=pause_reason_vo.description,
        )

    @inject()
    def list_pause_reason(
        self, repository: Provide[PauseReasonRepository]
    ) -> list[PauseReasonVo]:
        result: list = []
        for document in repository.list():
            result.append(
                PauseReasonVo(
                    pause_code=document["pause_code"],
                    description=document["description"],
                )
            )
        return result

    @inject
    def get_pause_reason(
        self, pause_code: str, repository: Provide[PauseReasonRepository]
    ) -> PauseReasonVo:
        pause_reason = repository.get_by_criteria({"pause_code": pause_code})
        return PauseReasonVo(
            pause_code=pause_reason["pause_code"],
            description=pause_reason["description"],
        )

    @inject
    def delete_pause_reason(
        self, pause_code: str, repository: Provide[PauseReasonRepository]
    ) -> PauseReasonVo:
        repository.delete_by_criteria({"pause_code": pause_code})
        return PauseReasonVo(pause_code=pause_code, description="")
