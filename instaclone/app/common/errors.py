from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED
)

class ExpiredSignatureError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "The token has expired.")

class InvalidTokenError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Invalid token.")

class BlockedTokenError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "The token has been blocked.")

class InvalidCredentialsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Invalid credentials.")