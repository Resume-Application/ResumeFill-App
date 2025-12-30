from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Union
from fastapi import Depends, HTTPException, status
from joserfc import jwt, jwk 
from joserfc.errors import BadSignatureError, InvalidPayloadError, ClaimError
from pydantic import BaseModel
from app.core.config import settings
from pwdlib import PasswordHash

import logging

logger = logging.getLogger(__name__)
password_hash = PasswordHash.recommended()
_key = jwk.import_key(settings.SECRET_KEY, "oct")

_claims_requests = jwt.JWTClaimsRegistry(
    iss={"essential": True, "value": settings.PROJECT_URL},
)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


def create_access_token(user_id:str, expires_delta: timedelta | None = None) -> TokenResponse:
    '''
    Docstring for create_access_token
    :param data: Description
    :type data: dict
    :param expires_delta: Timedelta for when access token expires. Default is 24 hours
    :type expires_delta: timedelta | None
    '''
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=24)

    header = {
        "alg": settings.JWT_ALGORITHM,
        "typ": "JWT"}
    claim = {
        "user": user_id,
        "exp": expire,
        "iss": settings.PROJECT_URL
    }
    encoded = jwt.encode(header, claim, _key)

    token = TokenResponse(
        access_token=encoded,
        token_type="bearer"
    )
    return token

async def decode_access_token(tokenResponse: TokenResponse) -> str | None:
    '''
    Returns the user id for a payload token or none if not valid. It is invalid if the timedate expired
    
    :param token: Description
    :type token: str
    :return: Description
    :rtype: dict
    '''
    encrypted = tokenResponse.access_token
    user = None
    try:
        token = jwt.decode(encrypted, _key)
    except BadSignatureError:
        logging.info("Bad signature")
        return None
    except InvalidPayloadError:
        logging.info("Bad payload")
        return None
        
    except Exception as e:
        logging.info(f"Bad signature {e}")
        return None
    try:
        _claims_requests.validate(token.claims)
    except ClaimError as error:
        logging.info(f"Claim error: {error.claim} {error.error} {error.description}")
        return None
    
    user = token.claims.get("user")
    return user

def verify_password(plain_password, hashed_password):
    '''
    Docstring for verify_password
    
    :param plain_password: Password string
    :param hashed_password: Hashed Password string
    '''
    return password_hash.verify(plain_password, hashed_password)

def hash_password(password):
    '''
    Returns a hashed password
    
    :param password: Description
    '''
    return password_hash.hash(password)