from AsteriskRealtimeData.application.peer_service import PeerService
from AsteriskRealtimeData.domain.peer.peer_vo import PeerVo


class PeerController:
    def create(self, peer: PeerVo) -> PeerVo:
        peer_parameter = PeerVo(**peer)
        return PeerService().create_peer(peer_parameter)

    def list(self) -> list[dict]:
        peers = PeerService().list_peer()
        result: list = []

        for peer in peers:
            result.append(peer.as_dict())

        return result

    def get_by_criteria(self, search_criteria: str) -> dict:
        return PeerService().get_peer(search_criteria).as_dict()

    def delete_by_criteria(self, search_criteria: str) -> dict:
        return PeerService().delete_peer(search_criteria)
