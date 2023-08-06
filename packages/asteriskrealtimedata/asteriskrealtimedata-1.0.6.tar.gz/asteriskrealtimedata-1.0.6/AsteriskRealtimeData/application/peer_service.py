from antidote import inject, Provide
from AsteriskRealtimeData.application.peer_repository import PeerRepository
from AsteriskRealtimeData.domain.peer.peer import Peer
from AsteriskRealtimeData.domain.peer.peer_vo import PeerVo


class PeerService:
    @inject
    def create_peer(
        self, peer_vo: PeerVo, repository: Provide[PeerRepository],
    ) -> PeerVo:

        peer = Peer(
            peer_name=peer_vo.peer_name,
            peer_type=peer_vo.peer_type,
            peer_ip_address=peer_vo.peer_ip_address,
        )

        repository.save(peer, {"peer_name": peer_vo.peer_name})

        return PeerVo(
            peer_name=peer_vo.peer_name,
            peer_type=peer_vo.peer_type,
            peer_ip_address=peer_vo.peer_ip_address,
        )

    @inject()
    def list_peer(self, repository: Provide[PeerRepository]) -> list[PeerVo]:
        result: list = []
        print(repository)
        for document in repository.list():
            result.append(
                PeerVo(
                    peer_name=document["peer_name"],
                    peer_type=document["peer_type"],
                    peer_ip_address=document["peer_ip_address"],
                )
            )
        return result

    @inject
    def get_peer(self, peer_name: str, repository: Provide[PeerRepository]) -> PeerVo:
        peer = repository.get_by_criteria({"peer_name": peer_name})
        return PeerVo(
            peer_name=peer["peer_name"],
            peer_type=peer["peer_type"],
            peer_ip_address=peer["peer_ip_address"],
        )

    @inject
    def delete_peer(
        self, peer_name: str, repository: Provide[PeerRepository]
    ) -> PeerVo:
        repository.delete_by_criteria({"peer_name": peer_name})
        return PeerVo(peer_name=peer_name, peer_type="", peer_ip_address="")
