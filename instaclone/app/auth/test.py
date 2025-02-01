import os
import httpx
import jwt
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from instaclone.database.google_settings import GOOGLE_SETTINGS
from instaclone.database.connection import SESSION
from instaclone.app.user.models import User
from sqlalchemy.future import select
from datetime import datetime, timedelta
from google.oauth2 import id_token
from google.auth.transport import requests
from instaclone.app.user.dto.responses import UserDetailResponse
from instaclone.database.annotation import transactional
from instaclone.app.auth.utils import (
    create_access_token,
    create_refresh_token,
    refresh_access_token
)

GOOGLE_CLIENT_ID = GOOGLE_SETTINGS.client_id
ACCESS_TOKEN_EXPIRE_MINUTES = 60

test_router = APIRouter()

class GoogleAuthRequest(BaseModel):
    credential: str

@test_router.post("/api/auth/google")
@transactional
async def google_login(payload: GoogleAuthRequest):
    try:
        # Verify Google token
        id_info = id_token.verify_oauth2_token(
            payload.credential, requests.Request(), GOOGLE_CLIENT_ID
        )
        
        email = id_info["email"]
        name = id_info["name"]
        picture = id_info.get("picture")

        async with SESSION() as session:
            stmt = select(User).filter_by(email=email)
            result = await session.execute(stmt)
            user = result.scalars().first()

            if not user:
                user = User(
                    full_name=name,
                    email=email,
                    username=name,
                    profile_image=picture,
                    password="default",
                    creation_date=datetime.today().date(),
                    social=True
                )
                session.add(user)
                await session.commit()

        access_token = create_access_token(user.user_id, expires=timedelta(minutes=10))
        refresh_token = create_refresh_token(user.user_id, expires=timedelta(hours=24))

        return UserSigninResponse(access_token=access_token, refresh_token=refresh_token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
