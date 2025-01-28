from instaclone.common.errors import InstacloneHttpException
from starlette.status import HTTP_413_REQUEST_ENTITY_TOO_LARGE, HTTP_400_BAD_REQUEST, HTTP_408_REQUEST_TIMEOUT

class FileSizeLimitError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_413_REQUEST_ENTITY_TOO_LARGE, "File is too large")

class FailedToSave(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "File did not save.")

class FailedToDelete(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_408_REQUEST_TIMEOUT, "Could not delete file.")