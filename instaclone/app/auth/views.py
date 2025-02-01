import os
import httpx
from fastapi import FastAPI, Depends, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi import Query
from instaclone.database.google_settings import GOOGLE_SETTINGS
from instaclone.app.auth.store import get_or_create_user_from_google

GOOGLE_CLIENT_ID = GOOGLE_SETTINGS.client_id
GOOGLE_CLIENT_SECRET = GOOGLE_SETTINGS.client_secret
GOOGLE_REDIRECT_URI = "https://waffle-instaclone.kro.kr/auth/callback"  # 설정한 리디렉션 URI

google_oauth_router = APIRouter()

@google_oauth_router.get("/login")
async def login():
    # Google OAuth 인증 URL 생성
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&response_type=code&scope=email%20profile"
    return google_auth_url


@google_oauth_router.get("/callback")
async def callback(code: str = Query(..., description="Google Authorization Code")):
    # Google API에 액세스 토큰 요청
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token")

        tokens = response.json()
        access_token = tokens.get("access_token")
        id_token = tokens.get("id_token")

    # Access token을 사용해 Google 사용자 정보 요청
    user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        user_info_response = await client.get(user_info_url, headers=headers)
        if user_info_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to retrieve user info")
        
        user_info = user_info_response.json()

    response = await get_or_create_user_from_google(user_info)
    
    # user와 is_created를 각각 받음
    user = response['user']
    is_created = response['is_created']
    return {
        "user_info": user_info,
        "user_id": user.user_id,
        "username": user.username,
        "user_password": user.password,
        "is_created": is_created
    }