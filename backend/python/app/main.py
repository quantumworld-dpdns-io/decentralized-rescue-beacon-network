import os

from fastapi import FastAPI

from .models import SignRequest, SignResponse, VerifyRequest, VerifyResponse
from .security import sign_payload, verify_payload

app = FastAPI(title="Beacon Network - Python Core")
SECRET_KEY = os.environ.get("HMAC_SECRET_KEY", "")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/sign", response_model=SignResponse)
def sign(req: SignRequest):
    signature, algorithm = sign_payload(req.payload, SECRET_KEY)
    return SignResponse(signature=signature, algorithm=algorithm)


@app.post("/verify", response_model=VerifyResponse)
def verify(req: VerifyRequest):
    valid = verify_payload(req.payload, req.signature, SECRET_KEY)
    return VerifyResponse(valid=valid)
