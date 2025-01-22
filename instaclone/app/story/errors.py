from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_413_REQUEST_ENTITY_TOO_LARGE

from instaclone.common.errors import InstacloneHttpException

class UserNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "User not found")

class StoryPermissionError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Don't have permission to delete story")

class StoryPermissionAccessError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Don't have access to story")

class StoryNotExistsError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "Story does not exist")

class StoryAlreadyExpired(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Story is already expired")

class FileSizeLimitError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_413_REQUEST_ENTITY_TOO_LARGE, "File is too large")
        
class HighlightDNEError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "Highlight does not exist")
        
class StoryViewPermissionError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Don't have permission to view story viewers")  

class StoryInHighlightsError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Story already added to highlight")

class HighlightNameError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Highlight name already exists")

class HighlightPermissionError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "Don't have permission to access highlight")

class UserAddedError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "User already added to this highlight")

class CannotRemoveError(InstacloneHttpException):
    def __init__(self, text: str) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, f"Cannot remove user from highlight: {text}")

class CannotChangeAdminError(InstacloneHttpException):
    def __init__(self, text: str) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, f"Cannot change highlight admin: {text}")

class CannotChangeHighlightNameError(InstacloneHttpException):
    def __init__(self, text: str) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, f"Cannot change highlight name: {text}")
        