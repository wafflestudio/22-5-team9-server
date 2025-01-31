from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from instaclone.api import api_router
from instaclone.app.auth.views import google_oauth_router

app = FastAPI()

app.include_router(api_router, prefix="/api")
app.include_router(google_oauth_router, prefix='/auth')

origins = [
    "https://d3l72zsyuz0duc.cloudfront.net",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/story_uploads", StaticFiles(directory="story_uploads"), name="story_uploads")
app.mount("/media_uploads", StaticFiles(directory="media_uploads"), name="media_uploads")

@app.get("/test")
def test_api():
    return "SUCCESS"