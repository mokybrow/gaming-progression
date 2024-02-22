from pydantic import UUID4, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class VerifyToken(BaseModel):
    verify_token: str
    token_type: str


class RecoveryToken(BaseModel):
    recovery_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    id: UUID4 | None = None
