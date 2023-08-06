from AsteriskRealtimeData.application.call_service import CallService
from AsteriskRealtimeData.domain.call.call_vo import CallVo


class CallController:
    def create(self, call: CallVo) -> CallVo:
        call_parameter = CallVo(**call)
        return CallService().create_call(call_parameter)

    def list(self) -> list[dict]:
        calls = CallService().list_call()
        result: list = []

        for call in calls:
            result.append(call.as_dict())

        return result

    def get_by_criteria(self, search_criteria: str) -> dict:
        return CallService().get_call(search_criteria).as_dict()

    def delete_by_criteria(self, search_criteria: str) -> dict:
        return CallService().delete_call(search_criteria)
