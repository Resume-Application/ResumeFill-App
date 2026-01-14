from pydantic import BaseModel

class JWTTokenClaims(BaseModel):
    user_id: int
    exp: int
    iss: str