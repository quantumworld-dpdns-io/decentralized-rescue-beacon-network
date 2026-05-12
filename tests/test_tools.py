import unittest

from src.rescue_beacon_network.models import BeaconPacket
from src.rescue_beacon_network.network import DecentralizedRescueBeaconNetwork
from src.rescue_beacon_network.security import HMACPacketSigner
from src.rescue_beacon_network.tools import BeaconNetworkToolBoundary


def _make_boundary() -> tuple[DecentralizedRescueBeaconNetwork, BeaconNetworkToolBoundary]:
    signer = HMACPacketSigner(secret="tool-test-secret")
    network = DecentralizedRescueBeaconNetwork(signer=signer)
    network.connect_nodes("A", "B")
    network.connect_nodes("B", "C")
    network.connect_nodes("C", "D")
    return network, BeaconNetworkToolBoundary(network)


class ToolBoundaryReadResourcesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.network, self.boundary = _make_boundary()
        self.signer = self.network._signer

    # ------------------------------------------------------------------
    # resource_registered_nodes
    # ------------------------------------------------------------------

    def test_resource_registered_nodes_returns_sorted_list(self) -> None:
        nodes = self.boundary.resource_registered_nodes()
        self.assertEqual(nodes, ["A", "B", "C", "D"])

    def test_resource_registered_nodes_emits_audit_event(self) -> None:
        self.boundary.resource_registered_nodes()
        events = self.boundary.audit_log()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].action, "resource_registered_nodes")
        self.assertEqual(events[0].details["node_count"], "4")

    def test_resource_registered_nodes_has_no_network_side_effects(self) -> None:
        metrics_before = self.network.metrics()
        self.boundary.resource_registered_nodes()
        metrics_after = self.network.metrics()
        self.assertEqual(metrics_before, metrics_after)

    # ------------------------------------------------------------------
    # resource_node_neighbors
    # ------------------------------------------------------------------

    def test_resource_node_neighbors_returns_correct_neighbors(self) -> None:
        neighbors = self.boundary.resource_node_neighbors("B")
        self.assertEqual(neighbors, ["A", "C"])

    def test_resource_node_neighbors_empty_for_unknown_node(self) -> None:
        neighbors = self.boundary.resource_node_neighbors("Z")
        self.assertEqual(neighbors, [])

    def test_resource_node_neighbors_emits_audit_event(self) -> None:
        self.boundary.resource_node_neighbors("B")
        events = self.boundary.audit_log()
        self.assertEqual(events[0].action, "resource_node_neighbors")
        self.assertEqual(events[0].details["node_id"], "B")
        self.assertEqual(events[0].details["neighbor_count"], "2")

    def test_resource_node_neighbors_has_no_network_side_effects(self) -> None:
        metrics_before = self.network.metrics()
        self.boundary.resource_node_neighbors("A")
        self.assertEqual(self.network.metrics(), metrics_before)

    # ------------------------------------------------------------------
    # resource_reachable_nodes
    # ------------------------------------------------------------------

    def test_resource_reachable_nodes_returns_reachable_within_hops(self) -> None:
        reachable = self.boundary.resource_reachable_nodes("A", max_hops=2)
        self.assertEqual(reachable, ["B", "C"])

    def test_resource_reachable_nodes_zero_hops_returns_empty(self) -> None:
        reachable = self.boundary.resource_reachable_nodes("A", max_hops=0)
        self.assertEqual(reachable, [])

    def test_resource_reachable_nodes_unknown_origin_returns_empty(self) -> None:
        reachable = self.boundary.resource_reachable_nodes("Z", max_hops=3)
        self.assertEqual(reachable, [])

    def test_resource_reachable_nodes_emits_audit_event(self) -> None:
        self.boundary.resource_reachable_nodes("A", max_hops=2)
        events = self.boundary.audit_log()
        self.assertEqual(events[0].action, "resource_reachable_nodes")
        self.assertEqual(events[0].details["origin_node_id"], "A")
        self.assertEqual(events[0].details["max_hops"], "2")
        self.assertEqual(events[0].details["reachable_count"], "2")

    def test_resource_reachable_nodes_does_not_consume_dedupe_slot(self) -> None:
        self.boundary.resource_reachable_nodes("A", max_hops=3)
        signer = self.network._signer
        packet = signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "test"}, max_hops=3))
        outcome = self.network.submit_distress_packet(packet)
        self.assertIsNone(outcome.dropped_reason)

    def test_resource_reachable_nodes_has_no_network_side_effects(self) -> None:
        metrics_before = self.network.metrics()
        self.boundary.resource_reachable_nodes("A", max_hops=3)
        self.assertEqual(self.network.metrics(), metrics_before)


class ToolBoundaryWriteToolsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.network, self.boundary = _make_boundary()
        self.signer = self.network._signer

    # ------------------------------------------------------------------
    # tool_submit_packet
    # ------------------------------------------------------------------

    def test_tool_submit_packet_delivers_to_reachable_nodes(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "medical"}, max_hops=2))
        outcome = self.boundary.tool_submit_packet(packet)
        self.assertEqual(outcome.delivered_nodes, ["B", "C"])

    def test_tool_submit_packet_emits_pre_and_post_audit_events(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "flood"}, max_hops=1))
        self.boundary.tool_submit_packet(packet)
        events = self.boundary.audit_log()
        actions = [e.action for e in events]
        self.assertIn("tool_submit_packet", actions)
        self.assertIn("tool_submit_packet_result", actions)

    def test_tool_submit_packet_audit_records_packet_id(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "fire"}, max_hops=1))
        self.boundary.tool_submit_packet(packet)
        pre = next(e for e in self.boundary.audit_log() if e.action == "tool_submit_packet")
        self.assertEqual(pre.details["packet_id"], packet.packet_id)

    def test_tool_submit_packet_result_records_delivered_count(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "storm"}, max_hops=2))
        self.boundary.tool_submit_packet(packet)
        result = next(e for e in self.boundary.audit_log() if e.action == "tool_submit_packet_result")
        self.assertEqual(result.details["delivered_count"], "2")
        self.assertEqual(result.details["dropped_reason"], "")

    def test_tool_submit_packet_result_records_drop_reason(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "bad"}, max_hops=0))
        self.boundary.tool_submit_packet(packet)
        result = next(e for e in self.boundary.audit_log() if e.action == "tool_submit_packet_result")
        self.assertEqual(result.details["dropped_reason"], "invalid_packet")

    def test_tool_submit_packet_increments_network_metrics(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "cold"}, max_hops=1))
        self.boundary.tool_submit_packet(packet)
        self.assertEqual(self.network.metrics()["submitted"], 1)

    def test_tool_submit_packet_with_target_filter(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "wave"}, max_hops=3))
        outcome = self.boundary.tool_submit_packet(packet, target_nodes=["D"])
        self.assertEqual(outcome.delivered_nodes, ["D"])

    # ------------------------------------------------------------------
    # tool_submit_packets (batch)
    # ------------------------------------------------------------------

    def test_tool_submit_packets_returns_batch_outcome(self) -> None:
        p1 = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "wind"}, max_hops=1, packet_id="p1"))
        p2 = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "rain"}, max_hops=1, packet_id="p2"))
        batch = self.boundary.tool_submit_packets([p1, p2])
        self.assertEqual(batch.delivered_packet_count, 2)
        self.assertEqual(batch.dropped_packet_count, 0)

    def test_tool_submit_packets_emits_batch_audit_events(self) -> None:
        p1 = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "quake"}, max_hops=1, packet_id="q1"))
        self.boundary.tool_submit_packets([p1])
        actions = [e.action for e in self.boundary.audit_log()]
        self.assertIn("tool_submit_packets", actions)
        self.assertIn("tool_submit_packets_result", actions)

    def test_tool_submit_packets_result_records_counts(self) -> None:
        good = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "ok"}, max_hops=1, packet_id="g1"))
        bad = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "ng"}, max_hops=0, packet_id="b1"))
        self.boundary.tool_submit_packets([good, bad])
        result = next(e for e in self.boundary.audit_log() if e.action == "tool_submit_packets_result")
        self.assertEqual(result.details["delivered_packet_count"], "1")
        self.assertEqual(result.details["dropped_packet_count"], "1")


class ToolBoundaryAuditLogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.network, self.boundary = _make_boundary()
        self.signer = self.network._signer

    def test_audit_log_limit_returns_last_n_events(self) -> None:
        self.boundary.resource_registered_nodes()
        self.boundary.resource_node_neighbors("A")
        self.boundary.resource_reachable_nodes("A", max_hops=1)
        events = self.boundary.audit_log(limit=2)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[-1].action, "resource_reachable_nodes")

    def test_audit_log_zero_limit_returns_empty(self) -> None:
        self.boundary.resource_registered_nodes()
        self.assertEqual(self.boundary.audit_log(limit=0), [])

    def test_audit_log_none_limit_returns_all(self) -> None:
        self.boundary.resource_registered_nodes()
        self.boundary.resource_registered_nodes()
        events = self.boundary.audit_log()
        self.assertEqual(len(events), 2)

    def test_audit_log_events_have_timestamps(self) -> None:
        self.boundary.resource_registered_nodes()
        event = self.boundary.audit_log()[0]
        self.assertIsNotNone(event.timestamp)

    def test_boundary_audit_log_is_separate_from_network_audit_log(self) -> None:
        packet = self.signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "sep"}, max_hops=1))
        self.boundary.tool_submit_packet(packet)
        boundary_actions = {e.action for e in self.boundary.audit_log()}
        network_actions = {e.action for e in self.network.audit_log()}
        self.assertTrue(boundary_actions.isdisjoint(network_actions))


if __name__ == "__main__":
    unittest.main()
