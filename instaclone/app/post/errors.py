from instaclone.common.errors import InstacloneHttpException
from starlette.status import HTTP_401_UNAUTHORIZED


class PostNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(404, "Post not found")

class PostDeleteError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Don't have permission to delete post")

class PostEditError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Don't have permission to edit post")