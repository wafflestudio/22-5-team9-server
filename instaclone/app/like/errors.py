from instaclone.common.errors import InstacloneHttpException

class AlreadyLikedError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(400, "Already liked")
        
class LikeNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(404, "Like not founding")

class LikeCreationError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(500, "Cannot create like")

class ContentNotFoundError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(404, "The requested content does not exist")

class SelfStoryLikeError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(400, "Cannot like your own story")