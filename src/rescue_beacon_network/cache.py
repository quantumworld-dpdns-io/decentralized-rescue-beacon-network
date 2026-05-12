from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, Optional


@dataclass
class _TTLRecord:
    value: Any
    expires_at: datetime


class InMemoryTTLStore:
    """Small Redis-like TTL key store for relay de-duplication."""

    def __init__(self, now_fn: Optional[Callable[[], datetime]] = None) -> None:
        self._now_fn = now_fn or (lambda: datetime.now(timezone.utc))
        self._records: Dict[str, _TTLRecord] = {}

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be > 0")
        self._records[key] = _TTLRecord(value=value, expires_at=self._now_fn() + timedelta(seconds=ttl_seconds))

    def get(self, key: str) -> Optional[Any]:
        self._prune_key(key)
        record = self._records.get(key)
        return record.value if record else None

    def contains(self, key: str) -> bool:
        return self.get(key) is not None

    def _prune_key(self, key: str) -> None:
        record = self._records.get(key)
        if record and self._now_fn() >= record.expires_at:
            self._records.pop(key, None)
