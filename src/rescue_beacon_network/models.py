from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4


@dataclass(frozen=True)
class BeaconPacket:
    """Distress packet propagated across relay nodes."""

    origin_node_id: str
    distress_payload: Dict[str, str]
    max_hops: int = 3
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    packet_id: str = field(default_factory=lambda: uuid4().hex)
    signature: Optional[str] = None
    signature_algorithm: Optional[str] = None


@dataclass(frozen=True)
class RelayOutcome:
    """Delivery summary for one distress packet submission."""

    packet_id: str
    delivered_nodes: List[str]
    routes: Dict[str, List[str]]
    dropped_reason: Optional[str] = None


@dataclass(frozen=True)
class BatchRelayOutcome:
    """Deterministically merged relay outcomes for a packet batch."""

    outcomes_by_packet_id: Dict[str, RelayOutcome]
    ordered_packet_ids: List[str]
    delivered_packet_count: int
    dropped_packet_count: int


@dataclass(frozen=True)
class AuditEvent:
    """Structured network audit event for observable relay operations."""

    timestamp: datetime
    packet_id: str
    action: str
    details: Dict[str, str]
