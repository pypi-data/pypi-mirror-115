from AsteriskRealtimeData.infrastructure.api.pause_reason_controller import (
    PauseReasonController,
)


class Api:
    class PauseReason:
        @staticmethod
        def create(pause_reason_dict: dict):
            return PauseReasonController().create(pause_reason_dict)

        @staticmethod
        def list():
            return PauseReasonController().list()

        @staticmethod
        def get_by_id(pause_code: str):
            return PauseReasonController().get_by_id(pause_code)

        @staticmethod
        def delete_by_id(pause_code: str):
            return PauseReasonController().delete_by_id("2222")
