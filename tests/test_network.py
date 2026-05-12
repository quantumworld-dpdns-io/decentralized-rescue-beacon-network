import unittest
from datetime import datetime, timedelta, timezone

from src.rescue_beacon_network.cache import InMemoryTTLStore
from src.rescue_beacon_network.models import BeaconPacket
from src.rescue_beacon_network.network import DecentralizedRescueBeaconNetwork
from src.rescue_beacon_network.security import HMACPacketSigner


class FakeClock:
    def __init__(self) -> None:
        self.now = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def tick(self, seconds: int) -> None:
        self.now = self.now + timedelta(seconds=seconds)

    def __call__(self) -> datetime:
        return self.now


class RescueBeaconNetworkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.signer = HMACPacketSigner(secret="rescue-secret")
        self.network = DecentralizedRescueBeaconNetwork(signer=self.signer)
        self.network.connect_nodes("A", "B")
        self.network.connect_nodes("B", "C")
        self.network.connect_nodes("C", "D")

    def test_packet_reaches_multi_hop_neighbors(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "medical"}, max_hops=2))

        outcome = self.network.submit_distress_packet(packet)

        self.assertEqual(outcome.delivered_nodes, ["B", "C"])
        self.assertEqual(outcome.routes["C"], ["A", "B", "C"])

    def test_target_filter_restricts_delivery(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "fire"}, max_hops=3))

        outcome = self.network.submit_distress_packet(packet, target_nodes=["D"])

        self.assertEqual(outcome.delivered_nodes, ["D"])
        self.assertEqual(outcome.routes["D"], ["A", "B", "C", "D"])

    def test_duplicate_packets_are_dropped(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "flood"}, max_hops=3))

        first = self.network.submit_distress_packet(packet)
        second = self.network.submit_distress_packet(packet)

        self.assertEqual(first.dropped_reason, None)
        self.assertEqual(second.dropped_reason, "duplicate_packet")

    def test_invalid_signature_is_rejected(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "tampered"}, max_hops=3))
        tampered = BeaconPacket(
            origin_node_id=packet.origin_node_id,
            distress_payload={"type": "tampered", "extra": "malicious"},
            max_hops=packet.max_hops,
            created_at=packet.created_at,
            packet_id=packet.packet_id,
            signature=packet.signature,
            signature_algorithm=packet.signature_algorithm,
        )

        outcome = self.network.submit_distress_packet(tampered)

        self.assertEqual(outcome.dropped_reason, "invalid_signature")

    def test_ttl_store_expires_records(self) -> None:
        clock = FakeClock()
        store = InMemoryTTLStore(now_fn=clock)
        store.set("beacon:packet:1", True, ttl_seconds=5)

        self.assertTrue(store.contains("beacon:packet:1"))
        clock.tick(6)
        self.assertFalse(store.contains("beacon:packet:1"))

    def test_metrics_are_recorded(self) -> None:
        valid_packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "storm"}, max_hops=1))
        duplicate_packet = valid_packet
        invalid_packet = BeaconPacket(origin_node_id="A", distress_payload={"type": "bad"}, max_hops=1)

        self.network.submit_distress_packet(valid_packet)
        self.network.submit_distress_packet(duplicate_packet)
        self.network.submit_distress_packet(invalid_packet)

        metrics = self.network.metrics()
        self.assertEqual(metrics["submitted"], 3)
        self.assertEqual(metrics["delivered"], 1)
        self.assertEqual(metrics["dropped_duplicate"], 1)
        self.assertEqual(metrics["dropped_invalid_signature"], 1)


if __name__ == "__main__":
    unittest.main()
