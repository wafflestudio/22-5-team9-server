from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from instaclone.api import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")

origins = [
    "https://d3l72zsyuz0duc.cloudfront.net/",
    "http://localhost:5173"
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