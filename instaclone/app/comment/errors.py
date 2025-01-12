from instaclone.common.errors import InstacloneHttpException

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

class CommentNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "Comment not exists")

class CommentPermissionError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Comment Permission Error")

class CommentLengthLimitError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Comment is too long")

class CommentServerError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")