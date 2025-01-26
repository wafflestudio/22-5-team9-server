from instaclone.common.errors import InstacloneHttpException
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST

class LocationNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "Location not found")

class AlreadyExistLocationTagError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_409_CONFLICT, "Location Tag already exists")

class FetchError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch tag information")

class LocationCreationError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_500_INTERNAL_SERVER_ERROR, "Cannot create location tag")

class SameTagError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Have already selected this location tag")