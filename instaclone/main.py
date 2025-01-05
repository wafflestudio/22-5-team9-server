from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from instaclone.api import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")

@app.get("/test")
def test_api():
    return "SUCCESS"