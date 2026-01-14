from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Union
from fastapi import Depends, HTTPException, status
from joserfc import jwt, jwk
from joserfc.jwt import Token
from joserfc.errors import BadSignatureError, InvalidPayloadError, ClaimError
from pydantic import BaseModel
from app.core.config import settings
from app.models.jwt_models import JWTTokenClaims
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


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> TokenResponse:
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
    claim = JWTTokenClaims(
        user_id=user_id,
        exp=int(expire.timestamp()),
        iss=settings.PROJECT_URL
    ).model_dump()
    encoded = jwt.encode(header, claim, _key)

    token = TokenResponse(
        access_token=encoded,
        token_type="bearer"
    )
    return token

def decode_access_token(access_token: str) -> JWTTokenClaims | None:
    '''
    Decodes the access token as a jwt object.
    
    :param token: User string
    :type token: str
    :return: JWT of the object.
    :rtype: Joserfc.jwt.Token
    '''

    if not isinstance(access_token, str):
        raise TypeError(
            f"access_token must be str, got {type(access_token).__name__}"
        )


    
    user = None
    try:
        token = jwt.decode(access_token, _key)
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
    
    claims = JWTTokenClaims.model_validate(token.claims)
    return claims

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