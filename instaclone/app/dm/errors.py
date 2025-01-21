from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from instaclone.common.errors import InstacloneHttpException

class ConnectionNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "Connection Not Found")

class InvalidTextFormatError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Invalid text format")

class InvalidTokenError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Invalid token")

class MissingHeaderError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Authorization header missing")

class InvalidHeaderFormatError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Invalid header format")

class MessageNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "Message not exists")

class MessagePermissionError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Permission error")