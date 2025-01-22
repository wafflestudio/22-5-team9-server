# instaclone/settings/google_settings.py
from pydantic_settings import BaseSettings
from instaclone.settings import SETTINGS

class GoogleSettings(BaseSettings):
    client_id: str = ""
    client_secret: str = ""

    class Config:
        case_sensitive = False
        env_prefix = "GOOGLE_"
        env_file = SETTINGS.env_file
        extra = "allow"  # extra 필드 허용

# GoogleSettings 인스턴스를 따로 초기화
GOOGLE_SETTINGS = GoogleSettings()
