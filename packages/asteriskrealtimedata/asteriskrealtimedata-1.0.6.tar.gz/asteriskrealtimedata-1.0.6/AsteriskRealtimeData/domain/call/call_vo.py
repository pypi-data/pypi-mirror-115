from datetime import datetime
from dataclasses import dataclass


@dataclass
class CallVo:
    peer_name: str
    client_id: str
    dialnumber: str
    lastevent: datetime
    track_id: str
    call_linkedid: str
    call_actor_address: str
    event_name: str
    origin_channel: str
    destination_channel: str
    origin_number: str
    destination_number: str

    def as_dict(self) -> dict:
        return self.__repr__()

    def __repr__(self):
        return {
            "id": self.get_id(),
            "peer_name": self.get_peer_name(),
            "client_id": self.get_client_id(),
            "dialnumber": self.get_dialnumber(),
            "lastevent": self.get_lastevent(),
            "track_id": self.get_track_id(),
            "call_linkedid": self.get_call_linkedid(),
            "call_actor_address": self.get_call_actor_address(),
            "event_name": self.get_event_name(),
            "origin_channel": self.get_origin_channel(),
            "destination_channel": self.get_destination_channel(),
            "origin_number": self.get_origin_number(),
            "destination_number": self.get_destination_number(),
        }
