from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import replace
from datetime import timezone

from .models import BeaconPacket


class HMACPacketSigner:
    """Crypto-agile packet signer with a PQC migration-compatible algorithm label."""

    def __init__(self, secret: str, algorithm_label: str = "ML-DSA-hybrid-simulated") -> None:
        self._secret = secret.encode("utf-8")
        self.algorithm_label = algorithm_label

    def sign(self, packet: BeaconPacket) -> BeaconPacket:
        digest = hmac.new(self._secret, self._canonicalize(packet), hashlib.sha256).hexdigest()
        return replace(packet, signature=digest, signature_algorithm=self.algorithm_label)

    def verify(self, packet: BeaconPacket) -> bool:
        if not packet.signature:
            return False
        expected = hmac.new(self._secret, self._canonicalize(packet), hashlib.sha256).hexdigest()
        return hmac.compare_digest(packet.signature, expected)

    @staticmethod
    def _canonicalize(packet: BeaconPacket) -> bytes:
        payload = {
            "packet_id": packet.packet_id,
            "origin_node_id": packet.origin_node_id,
            "distress_payload": packet.distress_payload,
            "max_hops": packet.max_hops,
            "created_at": packet.created_at.astimezone(timezone.utc).isoformat(),
        }
        return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
