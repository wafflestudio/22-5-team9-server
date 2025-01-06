from instaclone.common.errors import InstacloneHttpException


class PostNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(404, "Post not found")