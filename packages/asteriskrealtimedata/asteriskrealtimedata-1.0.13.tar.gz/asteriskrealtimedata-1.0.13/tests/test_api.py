from AsteriskRealtimeData.domain.call.call_vo import CallVo
from datetime import datetime
import unittest
from unittest.mock import MagicMock
from AsteriskRealtimeData.application.mascara_ipaddress_service import (
    MascaraIpaddressService,
)
from AsteriskRealtimeData.domain.queue_member.queue_member_vo import QueueMemberVo
from AsteriskRealtimeData.domain.queue_status.queue_status_vo import QueueStatusVo
from AsteriskRealtimeData.domain.peer.peer_vo import PeerVo
from AsteriskRealtimeData.domain.pause_reason.pause_reasons_vo import PauseReasonVo
from AsteriskRealtimeData.domain.mascara_ipaddress.mascara_ipaddress_vo import (
    MascaraIpaddressVo,
)
from AsteriskRealtimeData.api import Api


class TestAPI(unittest.TestCase):
    def test_pause_reason_list(self):
        Api.PauseReason.create(PauseReasonVo(pause_code="1111", description="aaaaaa"))
        Api.PauseReason.create(PauseReasonVo(pause_code="2222", description="bbbbbb"))
        print(Api.PauseReason.list())
        print(Api.PauseReason.get_by_pause_code("2222"))
        Api.PauseReason.delete_by_pause_code("2222")

    def test_mascara_ipaddress(self):
        Api.MascaraIpaddress.create(MascaraIpaddressVo(ipaddress="1.1.1.1"))
        Api.MascaraIpaddress.create(MascaraIpaddressVo(ipaddress="2.2.2.2"))
        print(Api.MascaraIpaddress.list())
        print(Api.MascaraIpaddress.get_by_ipaddress("1.1.1.1"))
        Api.MascaraIpaddress.delete_by_ipaddress("2.2.2.2")

    def test_peer(self):
        Api.Peer.create(
            PeerVo(peer_name="SIP/100", peer_type="SIP", peer_ip_address="1.1.1.1")
        )
        Api.Peer.create(
            PeerVo(peer_name="SIP/200", peer_type="SIP", peer_ip_address="2.2.2.2")
        )
        print(Api.Peer.list())
        print(Api.Peer.get_by_peer("SIP/100"))
        Api.Peer.delete_by_peer("SIP/200")

    def test_queue_status(self):
        Api.QueueStatus.create(
            QueueStatusVo(status_code="1", description="Estado de la cola 1")
        )
        Api.QueueStatus.create(
            QueueStatusVo(status_code="2", description="Estado de la cola 2")
        )
        print(Api.QueueStatus.list())
        print(Api.QueueStatus.get_by_status_code("1"))
        Api.QueueStatus.delete_by_status_code("2")

    def test_queue_member(self):
        mock_mascara_ipaddress_service = MascaraIpaddressService()
        mock_mascara_ipaddress_service.get_mascara_ipaddress = MagicMock(
            return_value="1.1.1.1"
        )
        Api.QueueMember.create(
            QueueMemberVo(
                peer="SIP/100",
                actual_status="1111",
                ipaddress="1.1.1.1",
                membername="Juca",
            )
        )

        mock_mascara_ipaddress_service_two = MascaraIpaddressService()
        mock_mascara_ipaddress_service_two.get_mascara_ipaddress = MagicMock(
            return_value="2.2.2.2"
        )
        Api.QueueMember.create(
            QueueMemberVo(
                peer="SIP/200",
                actual_status="2222",
                ipaddress="2.2.2.2",
                membername="Other",
            )
        )
        print(Api.QueueMember.list())
        print(Api.QueueMember.get_by_peer("SIP/100"))
        Api.QueueMember.delete_by_peer("SIP/200")

    def test_call(self):
        Api.Call.create(
            CallVo(
                peer_name="SIP/100",
                client_id="1000",
                dialnumber="222222222",
                lastevent=datetime.now(),
                track_id="1111",
                call_linkedid="1111",
                call_actor_address="actadd",
                event_name="evento",
                origin_channel="origchan",
                destination_channel="destchan",
                origin_number="1111111",
                destination_number="100",
            )
        )
        Api.Call.create(
            CallVo(
                peer_name="SIP/200",
                client_id="2000",
                dialnumber="333333333",
                lastevent=datetime.now(),
                track_id="1111",
                call_linkedid="2222",
                call_actor_address="actadd",
                event_name="evento",
                origin_channel="origchan",
                destination_channel="destchan",
                origin_number="1111111",
                destination_number="100",
            )
        )
        print(Api.Call.list())
        print(Api.Call.get_by_call_linkedid("1111"))
        Api.Call.delete_by_call_linkedid("2222")
