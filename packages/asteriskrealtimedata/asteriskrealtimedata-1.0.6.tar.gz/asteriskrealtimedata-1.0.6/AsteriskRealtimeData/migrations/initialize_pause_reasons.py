from AsteriskRealtimeData.domain.pause_reason.pause_reason import PauseReason
from AsteriskRealtimeData.api import Api


class InitializePauseReasons:
    def __init__(self) -> None:
        self.api = Api.PauseReason

    def initialize_pause_reasons(self):
        self.api.create({"pause_code": "100001", "description": "Conectado"})
        self.api.create({"pause_code": "100002", "description": "Disponible"})
        self.api.create({"pause_code": "200001", "description": "Desconectado"})
        self.api.create({"pause_code": "200002", "description": "En colación"})
        self.api.create({"pause_code": "200003", "description": "Baño"})
        self.api.create({"pause_code": "200004", "description": "En Reunión"})
        self.api.create({"pause_code": "200005", "description": "Atención vendedor"})
        self.api.create({"pause_code": "300001", "description": "Hablando"})
        self.api.create(
            {"pause_code": "300002", "description": "ACW (After Call Work)"}
        )
        self.api.create({"pause_code": "300003", "description": "Ocupado"})
        self.api.create({"pause_code": "300004", "description": "Recibiendo llamada"})
        self.api.create({"pause_code": "300005", "description": "Discando"})
        self.api.create({"pause_code": "000000", "description": "Estado desconocido"})


InitializePauseReasons().initialize_pause_reasons()
