from instaclone.common.errors import InstacloneHttpException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_408_REQUEST_TIMEOUT


class PostNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "Post not found")

class PostSaveFailedError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_408_REQUEST_TIMEOUT, "Could not save post")

class PostDeleteFailedError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_408_REQUEST_TIMEOUT, "Could not delete post")

class PostDeletePermissionError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Don't have permission to delete post")

class PostEditPermissionError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Don't have permission to edit post")