from instaclone.common.errors import InstacloneHttpException

from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

class CommentNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "Comment not exists")

class CommentPermissionError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Comment Permission Error")