from instaclone.common.errors import InstacloneHttpException


class EmailAlreadyExistsError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(409, "Email already exists")


class UsernameAlreadyExistsError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(409, "Username already exists")

class PhoneNumberAlreadyExistsError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(409, "Phone number already exists")

class UserUnsignedError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(401, "User is not signed in")


class PermissionDeniedError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(403, "User does not have permission")

class InvalidUsernameOrPasswordError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(401, "Invalid username or password")

class ExpiredSignatureError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(401, "Token expired")

class InvalidTokenError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(401, "Invalid token")

class BlockedTokenError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(401, "Blocked token")