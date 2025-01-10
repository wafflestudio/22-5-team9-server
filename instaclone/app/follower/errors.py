from instaclone.common.errors import InstacloneHttpException

class AlreadyFollowingError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(409, "Already following")

class FollowCreationError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(500, "Failed to create follow relationship")

class UserNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(404, "User not found")

class NotFollowingError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(400, "Not following the user")

class CannotFollowSelfError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(400, "Cannot follow yourself")