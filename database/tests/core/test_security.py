import pytest
from datetime import timedelta, datetime, timezone
from joserfc import jwt
import logging

from app.core.security import create_access_token, decode_access_token, _key, settings, TokenResponse

@pytest.mark.asyncio
async def test_create_and_decode_token():
    # Arrange
    user_id = "user_123"
    expires = timedelta(hours=1)
    
    # Act
    token = create_access_token(user_id, expires)
    decoded_user = await decode_access_token(token)

    # Assert
    assert decoded_user == user_id
    assert isinstance(token, TokenResponse)
    assert decoded_user == user_id

@pytest.mark.asyncio
async def test_token_expiration():
    # Create a token that expires immediately
    token = create_access_token("user_expired", expires_delta=timedelta(seconds=-1))

    ce = None
    decoded_user= None
    try:
        decoded_user = await decode_access_token(token)
    except Exception as e:
        ce = e
    assert ce is not None
    assert decoded_user is None

@pytest.mark.asyncio
async def test_invalid_token():
    # Arrange: tampered token
    token = create_access_token("user_123")
    token.access_token = token.access_token + "tamper"

    # Act
    decoded_user = await decode_access_token(token)

    # Assert
    assert decoded_user is None

@pytest.mark.asyncio
async def test_claim_validation():
    # Arrange: token missing "user" claim
    user_id="user_123"
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

    decoded_user = await decode_access_token(token)

    # Assert
    assert decoded_user is None
