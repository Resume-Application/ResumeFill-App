import pytest
from datetime import timedelta, datetime, timezone
from joserfc import jwt
import logging

from app.core.security import create_access_token, decode_access_token, _key, settings, TokenResponse
from app.models.jwt_models import JWTTokenClaims

@pytest.mark.asyncio
async def test_create_and_decode_token():
    # Arrange
    user_id = 12345
    expires = timedelta(hours=1)
    
    # Act
    token = create_access_token(user_id, expires)
    decoded_token = decode_access_token(token)

    # Assert
    assert decoded_token is not None
    assert isinstance(token, TokenResponse)
    assert isinstance(decoded_token, JWTTokenClaims)

@pytest.mark.asyncio
async def test_token_expiration():
    # Create a token that expires immediately
    token = create_access_token(12345, expires_delta=timedelta(seconds=-1))

    ce = None
    try:
        decoded_token = decode_access_token(token)
            
    except Exception as e:
        ce = e
    assert ce is not None

@pytest.mark.asyncio
async def test_invalid_token():
    # Arrange: tampered token
    token = create_access_token(123450)
    token.access_token = token.access_token + "tamper"

    # Act
    decoded_token = decode_access_token(token)

    # Assert
    assert decoded_token is None

@pytest.mark.asyncio
async def test_claim_validation():
    # Arrange: token missing "user" claim
    user_id=12345
    expire = datetime.now(timezone.utc) + timedelta(hours=24)

    header = {
        "alg": settings.JWT_ALGORITHM,
        "typ": "JWT"}
    claim = {
        "user": user_id,
        "exp": expire,
        "iss": "FAKE ISSUER!"
    }
    encoded = jwt.encode(header, claim, _key)
    token = TokenResponse(
        access_token=encoded,
        token_type="bearer"
    )

    decoded_token = decode_access_token(token)

    # Assert
    assert decoded_token is None