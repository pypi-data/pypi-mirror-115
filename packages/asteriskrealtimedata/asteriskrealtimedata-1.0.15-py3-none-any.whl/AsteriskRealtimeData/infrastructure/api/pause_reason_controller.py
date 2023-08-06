from AsteriskRealtimeData.application.pause_reasons_service import PauseReasonService
from AsteriskRealtimeData.domain.pause_reason.pause_reasons_vo import PauseReasonVo


class PauseReasonController:
    def create(self, pause_reason_vo: PauseReasonVo) -> PauseReasonVo:
        return PauseReasonService().create_pause_reason(pause_reason_vo)

    def list(self) -> list[dict]:
        pause_reasons = PauseReasonService().list_pause_reason()
        result: list = []

        for pause_reason in pause_reasons:
            result.append(pause_reason.as_dict())

        return result

    def get_by_pause_code(self, pause_code: str) -> dict:
        return PauseReasonService().get_pause_reason(pause_code).as_dict()

    def get_by_search_criteria(self, search_criteria: str) -> dict:
        return PauseReasonService().get_by_search_criteria(search_criteria).as_dict()

    def delete_by_pause_code(self, pause_code: str) -> dict:
        return PauseReasonService().delete_pause_reason(pause_code)
