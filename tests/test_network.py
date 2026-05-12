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
        self.assertEqual(metrics["dropped_invalid_packet"], 0)

    def test_invalid_packet_is_rejected(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "medical"}, max_hops=0))

        outcome = self.network.submit_distress_packet(packet)

        self.assertEqual(outcome.dropped_reason, "invalid_packet")
        self.assertEqual(self.network.metrics()["dropped_invalid_packet"], 1)

    def test_deterministic_route_selection_with_multiple_equal_paths(self) -> None:
        network = DecentralizedRescueBeaconNetwork(signer=self.signer)
        network.connect_nodes("A", "C")
        network.connect_nodes("A", "B")
        network.connect_nodes("B", "D")
        network.connect_nodes("C", "D")
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "medical"}, max_hops=2))

        outcome = network.submit_distress_packet(packet, target_nodes=["D"])

        self.assertEqual(outcome.routes["D"], ["A", "B", "D"])

    def test_batch_submission_is_deterministic_and_summarized(self) -> None:
        packet_b = self.signer.sign(
            BeaconPacket(origin_node_id="A", distress_payload={"type": "fire"}, max_hops=1, packet_id="b-packet")
        )
        packet_a = self.signer.sign(
            BeaconPacket(origin_node_id="A", distress_payload={"type": "flood"}, max_hops=1, packet_id="a-packet")
        )
        packet_invalid = self.signer.sign(
            BeaconPacket(origin_node_id="A", distress_payload={"type": "invalid"}, max_hops=0, packet_id="c-packet")
        )

        batch = self.network.submit_distress_packets([packet_b, packet_invalid, packet_a])

        self.assertEqual(batch.ordered_packet_ids, ["a-packet", "b-packet", "c-packet"])
        self.assertEqual(batch.delivered_packet_count, 2)
        self.assertEqual(batch.dropped_packet_count, 1)
        self.assertEqual(batch.outcomes_by_packet_id["c-packet"].dropped_reason, "invalid_packet")

    def test_audit_log_captures_submit_events(self) -> None:
        delivered_packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "storm"}, max_hops=1))
        dropped_packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "storm"}, max_hops=0))

        self.network.submit_distress_packet(delivered_packet)
        self.network.submit_distress_packet(dropped_packet)

        events = self.network.audit_log()
        self.assertGreaterEqual(len(events), 4)
        self.assertEqual(events[-1].action, "submit_dropped")
        self.assertEqual(events[-1].details["reason"], "invalid_packet")


if __name__ == "__main__":
    unittest.main()
