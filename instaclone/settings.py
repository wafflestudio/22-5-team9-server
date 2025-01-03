import os

from pydantic_settings import BaseSettings

ENV = os.getenv("ENV", "local")
assert ENV in ("local", "test", "prod")


class Settings(BaseSettings):
    @property
    def is_local(self) -> bool:
        return ENV == "local"

    @property
    def is_prod(self) -> bool:
        return ENV == "prod"

    @property
    def env_file(self) -> str:
        return f".env.{ENV}"


SETTINGS = Settings()