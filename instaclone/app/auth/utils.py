from datetime import datetime, timedelta, timezone
from uuid import uuid4

from instaclone.app.common.errors import (
    ExpiredSignatureError,
    InvalidTokenError,
    BlockedTokenError
)

import jwt

SECRET_KEY = "secret_for_jwt"

def create_access_token(username: str, expires: timedelta) -> str:
    """
    access token을 생성합니다.
    """
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + expires,
        "type": "access"
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    return access_token

def create_refresh_token(username: str, expires: timedelta) -> str:
    """
    refresh token을 생성합니다.
    """
    payload = {
        "sub": username,
        "jti": uuid4().hex,
        "exp": datetime.now(timezone.utc) + expires,
        "type": "refresh"
    }
    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    return refresh_token

def validate_access_token(access_token: str) -> str:
    """
    access token을 검증하고 username을 반환합니다.
    """
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithm="HS256")
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
    
    if payload["type"] != "access":
        raise InvalidTokenError()
    
    return payload["sub"]

async def validate_refresh_token(refresh_token: str) -> str:
    """
    refresh token을 검증하고 username을 반환합니다.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithm="HS256")
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
    
    if payload["type"] != "refresh":
        raise InvalidTokenError()
    if await is_token_blocked(payload["jti"]):
        raise BlockedTokenError()
    
    return payload["sub"]

async def refresh_access_token(refresh_token: str, expires: timedelta) -> str:
    """
    refresh token으로 새로운 access token을 생성합니다.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithm="HS256")
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
    to_encode = {
        "sub": payload["sub"],
        "exp": datetime.now(timezone.utc) + expires,
        "type": "access"
    }
    await block_refresh_token(refresh_token)
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

    return access_token

async def block_refresh_token(refresh_token: str) -> None:
    """
    주어진 refresh token을 만료시킵니다.
    """
    pass

async def is_token_blocked(jti: str) -> bool:
    """
    refresh token이 만료되어 있는지 확인합니다.
    """
    pass