"""MCP-style tool boundary for the rescue beacon network.

Separates read-only topology resources from write-capable packet submission
tools, following MCP's principle of explicit, auditable action boundaries.

Every tool and resource access is recorded as a structured audit event so
callers can inspect the full operation trail without coupling to network
internals.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from .models import AuditEvent, BatchRelayOutcome, BeaconPacket, RelayOutcome
from .network import DecentralizedRescueBeaconNetwork

NO_PACKET_ID = "N/A"


class BeaconNetworkToolBoundary:
    """MCP-style interface over a DecentralizedRescueBeaconNetwork.

    Read-only resources (prefixed ``resource_``) inspect topology without
    modifying state.  Write-capable tools (prefixed ``tool_``) submit packets
    and produce observable side-effects.  All calls emit structured
    :class:`~rescue_beacon_network.models.AuditEvent` records that can be
    retrieved via :meth:`audit_log`.
    """

    def __init__(self, network: DecentralizedRescueBeaconNetwork) -> None:
        self._network = network
        self._boundary_audit: List[AuditEvent] = []

    # ------------------------------------------------------------------
    # Read-only topology resources
    # ------------------------------------------------------------------

    def resource_registered_nodes(self) -> List[str]:
        """Return sorted list of all registered node IDs (read-only)."""
        nodes = sorted(self._network._nodes.keys())
        self._emit("resource_registered_nodes", {"node_count": str(len(nodes))})
        return nodes

    def resource_node_neighbors(self, node_id: str) -> List[str]:
        """Return sorted neighbors of *node_id* (read-only).

        Returns an empty list when *node_id* is not registered.
        """
        neighbors = sorted(self._network._nodes.get(node_id, set()))
        self._emit(
            "resource_node_neighbors",
            {"node_id": node_id, "neighbor_count": str(len(neighbors))},
        )
        return neighbors

    def resource_reachable_nodes(self, origin_node_id: str, max_hops: int) -> List[str]:
        """Return nodes reachable from *origin_node_id* within *max_hops* (read-only).

        Does not submit a packet; no side-effects on network state.
        Returns an empty list when the origin is not registered or ``max_hops <= 0``.
        """
        if max_hops <= 0 or origin_node_id not in self._network._nodes:
            self._emit(
                "resource_reachable_nodes",
                {"origin_node_id": origin_node_id, "max_hops": str(max_hops), "reachable_count": "0"},
            )
            return []
        routes = self._network._find_routes(origin_node_id, max_hops)
        reachable = sorted(set(routes.keys()) - {origin_node_id})
        self._emit(
            "resource_reachable_nodes",
            {
                "origin_node_id": origin_node_id,
                "max_hops": str(max_hops),
                "reachable_count": str(len(reachable)),
            },
        )
        return reachable

    # ------------------------------------------------------------------
    # Write-capable packet submission tools
    # ------------------------------------------------------------------

    def tool_submit_packet(
        self,
        packet: BeaconPacket,
        target_nodes: Optional[List[str]] = None,
    ) -> RelayOutcome:
        """Submit *packet* to the network (write – has side-effects)."""
        self._emit(
            "tool_submit_packet",
            {
                "packet_id": packet.packet_id,
                "origin_node_id": packet.origin_node_id,
                "target_nodes": ",".join(target_nodes) if target_nodes else "",
            },
            packet_id=packet.packet_id,
        )
        outcome = self._network.submit_distress_packet(packet, target_nodes=target_nodes)
        self._emit(
            "tool_submit_packet_result",
            {
                "packet_id": packet.packet_id,
                "dropped_reason": outcome.dropped_reason or "",
                "delivered_count": str(len(outcome.delivered_nodes)),
            },
            packet_id=packet.packet_id,
        )
        return outcome

    def tool_submit_packets(
        self,
        packets: List[BeaconPacket],
        target_nodes_by_packet_id: Optional[Dict[str, List[str]]] = None,
    ) -> BatchRelayOutcome:
        """Submit a batch of packets deterministically (write – has side-effects)."""
        self._emit(
            "tool_submit_packets",
            {"packet_count": str(len(packets))},
        )
        batch = self._network.submit_distress_packets(packets, target_nodes_by_packet_id=target_nodes_by_packet_id)
        self._emit(
            "tool_submit_packets_result",
            {
                "delivered_packet_count": str(batch.delivered_packet_count),
                "dropped_packet_count": str(batch.dropped_packet_count),
            },
        )
        return batch

    # ------------------------------------------------------------------
    # Audit log
    # ------------------------------------------------------------------

    def audit_log(self, limit: Optional[int] = None) -> List[AuditEvent]:
        """Return boundary-level audit events (most-recent last).

        Pass *limit* to restrict to the last N events.
        """
        if limit is not None and limit <= 0:
            return []
        if limit is None:
            return list(self._boundary_audit)
        return list(self._boundary_audit[-limit:])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _emit(
        self,
        action: str,
        details: Optional[Dict[str, str]] = None,
        packet_id: str = NO_PACKET_ID,
    ) -> None:
        self._boundary_audit.append(
            AuditEvent(
                timestamp=datetime.now(timezone.utc),
                packet_id=packet_id,
                action=action,
                details=details or {},
            )
        )
