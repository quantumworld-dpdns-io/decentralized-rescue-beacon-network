from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from .cache import InMemoryTTLStore
from .models import BeaconPacket, RelayOutcome
from .security import HMACPacketSigner


@dataclass
class _Metrics:
    submitted: int = 0
    delivered: int = 0
    dropped_duplicate: int = 0
    dropped_invalid_signature: int = 0
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
            "dropped_unreachable": self._metrics.dropped_unreachable,
        }

    def submit_distress_packet(self, packet: BeaconPacket, target_nodes: Optional[List[str]] = None) -> RelayOutcome:
        self._metrics.submitted += 1

        if packet.origin_node_id not in self._nodes:
            self._metrics.dropped_unreachable += 1
            return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=[], routes={}, dropped_reason="origin_not_registered")

        if self._signer and not self._signer.verify(packet):
            self._metrics.dropped_invalid_signature += 1
            return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=[], routes={}, dropped_reason="invalid_signature")

        dedupe_key = f"beacon:packet:{packet.packet_id}"
        if self._dedupe_store.contains(dedupe_key):
            self._metrics.dropped_duplicate += 1
            return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=[], routes={}, dropped_reason="duplicate_packet")

        self._dedupe_store.set(dedupe_key, True, ttl_seconds=self._dedupe_ttl_seconds)

        routes = self._find_routes(packet.origin_node_id, packet.max_hops)
        candidate_nodes = set(routes.keys()) - {packet.origin_node_id}
        if target_nodes is not None:
            candidate_nodes &= set(target_nodes)

        delivered_nodes = sorted(candidate_nodes)
        if not delivered_nodes:
            self._metrics.dropped_unreachable += 1
            return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=[], routes={}, dropped_reason="no_reachable_targets")

        self._metrics.delivered += len(delivered_nodes)
        delivered_routes = {node_id: routes[node_id] for node_id in delivered_nodes}
        return RelayOutcome(packet_id=packet.packet_id, delivered_nodes=delivered_nodes, routes=delivered_routes)

    def _find_routes(self, origin_node_id: str, max_hops: int) -> Dict[str, List[str]]:
        routes: Dict[str, List[str]] = {origin_node_id: [origin_node_id]}
        queue = deque([(origin_node_id, 0)])

        while queue:
            node_id, hops = queue.popleft()
            if hops >= max_hops:
                continue
            for neighbor in self._nodes.get(node_id, set()):
                if neighbor in routes:
                    continue
                routes[neighbor] = [*routes[node_id], neighbor]
                queue.append((neighbor, hops + 1))

        return routes
