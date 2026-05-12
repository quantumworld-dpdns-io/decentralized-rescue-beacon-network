import hashlib
import hmac
import json


def sign_payload(payload: dict, secret_key: str) -> tuple[str, str]:
    canonical = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    secret = secret_key.encode("utf-8")
    signature = hmac.new(secret, canonical, hashlib.sha256).hexdigest()
    return signature, "HMAC-SHA256"


def verify_payload(payload: dict, signature: str, secret_key: str) -> bool:
    expected, _ = sign_payload(payload, secret_key)
    return hmac.compare_digest(signature, expected)
