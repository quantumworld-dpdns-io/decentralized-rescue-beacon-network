from pydantic import BaseModel


class SignRequest(BaseModel):
    payload: dict


class SignResponse(BaseModel):
    signature: str
    algorithm: str


class VerifyRequest(BaseModel):
    payload: dict
    signature: str


class VerifyResponse(BaseModel):
    valid: bool
