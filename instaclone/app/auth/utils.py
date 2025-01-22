from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlalchemy.sql import select
from instaclone.database.connection import SESSION
from instaclone.app.user.models import BlockedToken
from fastapi import WebSocket

from instaclone.app.user.models import User
from instaclone.common.errors import (
    ExpiredSignatureError,
    InvalidTokenError,
    BlockedTokenError
)
from instaclone.app.dm.errors import MissingHeaderError, InvalidHeaderFormatError, InvalidTokenError

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
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
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
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
    
    if payload["type"] != "refresh":
        raise InvalidTokenError()
    if await is_token_blocked(payload["jti"]):
        raise BlockedTokenError()
    
    return payload["sub"]

async def refresh_access_token(refresh_token: str, access_expires: timedelta, refresh_expires: timedelta) -> tuple[str, str]:
    """
    refresh token으로 새로운 access token을 생성합니다.
    access token, refresh token을 반환합니다.
    """
    username = await validate_refresh_token(refresh_token)
    to_encode = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + access_expires,
        "type": "access"
    }
    await block_refresh_token(refresh_token)
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    refresh_token = create_refresh_token(username, expires=refresh_expires)

    return access_token, refresh_token

async def block_refresh_token(refresh_token: str) -> str:
    """
    주어진 refresh token을 만료시킵니다.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
    
    if await is_token_blocked(payload["jti"]):
        raise BlockedTokenError()
    
    block_token = BlockedToken(jti=payload["jti"])
    SESSION.add(block_token)
    await SESSION.commit()
    return "SUCCESS"

async def is_token_blocked(jti: str) -> bool:
    """
    refresh token이 만료되어 있는지 확인합니다.
    """
    token = await SESSION.scalar(select(BlockedToken).where(BlockedToken.jti == jti))
    if token:
        return True
    else:
        return False
    
async def ws_login_with_header(websocket: WebSocket) -> User:
    token_prefix = "Bearer "
    authorization = websocket.headers.get("authorization")
    if not authorization:
        raise MissingHeaderError()
    
    if not authorization.startswith(token_prefix):
        raise InvalidHeaderFormatError()
    
    token = authorization[len(token_prefix):]
    username = validate_access_token(token)
    user = await SESSION.scalar(select(User).where(User.username == username))
    if not user:
        raise InvalidTokenError()
    return user