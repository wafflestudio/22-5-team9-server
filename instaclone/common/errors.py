from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class InstacloneHttpException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


class InvalidFieldFormatError(InstacloneHttpException):
    def __init__(self, detail: str | None = None) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, f"Invalid field format. {detail}")


class MissingRequiredFieldError(InstacloneHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Missing required fields")