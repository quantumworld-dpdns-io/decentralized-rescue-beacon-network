from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

from .cache import InMemoryTTLStore
from .models import AuditEvent, BatchRelayOutcome, BeaconPacket, RelayOutcome
from .security import HMACPacketSigner


@dataclass
class _Metrics:
    submitted: int = 0
    delivered: int = 0
    dropped_duplicate: int = 0
    dropped_invalid_signature: int = 0
    dropped_invalid_packet: int = 0
    dropped_unreachable: int = 0


class DecentralizedRescueBeaconNetwork:
    """In-memory multi-hop distress relay network."""

    def __init__(
        self,
        dedupe_ttl_seconds: int = 300,
        dedupe_store: Optional[InMemoryTTLStore] = None,
        signer: Optional[HMACPacketSigner] = None,
    ) -> None:
        self._nodes: Dict[str, Set[str]] = {}
        self._dedupe_ttl_seconds = dedupe_ttl_seconds
        self._dedupe_store = dedupe_store or InMemoryTTLStore()
        self._signer = signer
        self._metrics = _Metrics()
        self._audit_log: List[AuditEvent] = []

    def register_node(self, node_id: str) -> None:
        self._nodes.setdefault(node_id, set())

    def connect_nodes(self, left_node_id: str, right_node_id: str) -> None:
        self.register_node(left_node_id)
        self.register_node(right_node_id)
        self._nodes[left_node_id].add(right_node_id)
        self._nodes[right_node_id].add(left_node_id)

    def metrics(self) -> Dict[str, int]:
        return {
            "submitted": self._metrics.submitted,
            "delivered": self._metrics.delivered,
            "dropped_duplicate": self._metrics.dropped_duplicate,
            "dropped_invalid_signature": self._metrics.dropped_invalid_signature,
            "dropped_invalid_packet": self._metrics.dropped_invalid_packet,
            "dropped_unreachable": self._metrics.dropped_unreachable,
        }

    def submit_distress_packet(self, packet: BeaconPacket, target_nodes: Optional[List[str]] = None) -> RelayOutcome:
        self._metrics.submitted += 1
        self._record_event(packet.packet_id, "submit_received")

        if not self._is_valid_packet(packet):
            self._metrics.dropped_invalid_packet += 1
            self._record_event(packet.packet_id, "submit_dropped", {"reason": "invalid_packet"})
            return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=[], routes={}, dropped_reason="invalid_packet")

        if packet.origin_node_id not in self._nodes:
            self._metrics.dropped_unreachable += 1
            self._record_event(packet.packet_id, "submit_dropped", {"reason": "origin_not_registered"})
            return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=[], routes={}, dropped_reason="origin_not_registered")

        if self._signer and not self._signer.verify(packet):
            self._metrics.dropped_invalid_signature += 1
            self._record_event(packet.packet_id, "submit_dropped", {"reason": "invalid_signature"})
            return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=[], routes={}, dropped_reason="invalid_signature")

        dedupe_key = f"beacon:packet:{packet.packet_id}"
        if self._dedupe_store.contains(dedupe_key):
            self._metrics.dropped_duplicate += 1
            self._record_event(packet.packet_id, "submit_dropped", {"reason": "duplicate_packet"})
            return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=[], routes={}, dropped_reason="duplicate_packet")

        self._dedupe_store.set(dedupe_key, True, ttl_seconds=self._dedupe_ttl_seconds)

        routes = self._find_routes(packet.origin_node_id, packet.max_hops)
        candidate_nodes = set(routes.keys()) - {packet.origin_node_id}
        if target_nodes is not None:
            candidate_nodes &= set(target_nodes)

        delivered_nodes = sorted(candidate_nodes)
        if not delivered_nodes:
            self._metrics.dropped_unreachable += 1
            self._record_event(packet.packet_id, "submit_dropped", {"reason": "no_reachable_targets"})
            return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=[], routes={}, dropped_reason="no_reachable_targets")

        self._metrics.delivered += len(delivered_nodes)
        delivered_routes = {node_id: routes[node_id] for node_id in delivered_nodes}
        self._record_event(packet.packet_id, "submit_delivered", {"delivered_nodes": ",".join(delivered_nodes)})
        return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=delivered_nodes, routes=delivered_routes)

    def submit_distress_packets(
        self,
        packets: List[BeaconPacket],
        target_nodes_by_packet_id: Optional[Dict[str, List[str]]] = None,
    ) -> BatchRelayOutcome:
        outcomes_by_packet_id: Dict[str, RelayOutcome] = {}
        delivered_packet_count = 0
        dropped_packet_count = 0
        ordered_packets = sorted(packets, key=lambda packet: packet.packet_id)

        for packet in ordered_packets:
            target_nodes = None
            if target_nodes_by_packet_id is not None:
                target_nodes = target_nodes_by_packet_id.get(packet.packet_id)
            outcome = self.submit_distress_packet(packet, target_nodes=target_nodes)
            outcomes_by_packet_id[packet.packet_id] = outcome
            if outcome.dropped_reason is None:
                delivered_packet_count += 1
            else:
                dropped_packet_count += 1

        return BatchRelayOutcome(
            outcomes_by_packet_id=outcomes_by_packet_id,
            ordered_packet_ids=[packet.packet_id for packet in ordered_packets],
            delivered_packet_count=delivered_packet_count,
            dropped_packet_count=dropped_packet_count,
        )

    def audit_log(self, limit: Optional[int] = None) -> List[AuditEvent]:
        if limit is not None and limit <= 0:
            return []
        if limit is None:
            return list(self._audit_log)
        return list(self._audit_log[-limit:])

    def _find_routes(self, origin_node_id: str, max_hops: int) -> Dict[str, List[str]]:
        routes: Dict[str, List[str]] = {origin_node_id: [origin_node_id]}
        queue = deque([(origin_node_id, 0)])

        while queue:
            node_id, hops = queue.popleft()
            if hops >= max_hops:
                continue
            for neighbor in sorted(self._nodes.get(node_id, set())):
                if neighbor in routes:
                    continue
                routes[neighbor] = [*routes[node_id], neighbor]
                queue.append((neighbor, hops + 1))

        return routes

    @staticmethod
    def _is_valid_packet(packet: BeaconPacket) -> bool:
        """Validate packet boundary inputs before relay processing.

        A packet is valid when:
        - origin_node_id is not blank/whitespace
        - max_hops is a positive integer (> 0)
        """
        if not packet.origin_node_id.strip():
            return False
        if packet.max_hops <= 0:
            return False
        return True

    def _record_event(self, packet_id: str, action: str, details: Optional[Dict[str, str]] = None) -> None:
        self._audit_log.append(
            AuditEvent(
                timestamp=datetime.now(timezone.utc),
                packet_id=packet_id,
                action=action,
                details=details or {},
            )
        )
