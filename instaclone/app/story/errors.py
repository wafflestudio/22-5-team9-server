from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from instaclone.common.errors import InstacloneHttpException

class UserNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "User not found")

class StoryPermissionError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Don't have permission to delete story")

class StoryNotExistsError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "Story does not exist")

class StoryAlreadyExpired(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Story is already expired")