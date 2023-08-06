from AsteriskRealtimeData.application.peer_service import PeerService
from AsteriskRealtimeData.domain.peer.peer_vo import PeerVo


class PeerController:
    def create(self, peer_vo: PeerVo) -> PeerVo:
        return PeerService().create_peer(peer_vo)

    def list(self) -> list[dict]:
        peers = PeerService().list_peer()
        result: list = []

        for peer in peers:
            result.append(peer.as_dict())

        return result

    def get_by_peer(self, peer: str) -> dict:
        return PeerService().get_peer(peer).as_dict()

    def delete_by_peer(self, peer: str) -> dict:
        return PeerService().delete_peer(peer)
