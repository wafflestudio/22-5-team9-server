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

GOOGLE_CLIENT_ID = GOOGLE_SETTINGS.client_id
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

test_router = APIRouter()

class GoogleAuthRequest(BaseModel):
    credential: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

@test_router.post("/api/auth/google")
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
                    email=email,
                    username=name,
                    profile_image=picture,
                    password="default",
                    creation_date=datetime.today().date(),
                    social=True
                )
                session.add(user)
                await session.commit()

        # Generate JWT tokens
        access_token = create_access_token({"sub": user.user_id})

        return {
            "access_token": access_token,
            "user": {
                "id": user.user_id,
                "email": user.email,
                "username": user.username,
                "profile_image": user.profile_image
            }
        }
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
