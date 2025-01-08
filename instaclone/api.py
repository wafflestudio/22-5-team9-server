from fastapi import APIRouter

# from instaclone.app.comment.views import comment_router
# from instaclone.app.follower.views import follower_router
# from instaclone.app.medium.views import medium_router
from instaclone.app.post.views import post_router
from instaclone.app.story.views import story_router
from instaclone.app.user.views import user_router

api_router = APIRouter()

# api_router.include_router(comment_router, prefix="/comments", tags=["comments"])
# api_router.include_router(follower_router, prefix="/follower", tags=["follower"])
# api_router.include_router(medium_router, prefix="/medium", tags=["medium"])
api_router.include_router(post_router, prefix="/post", tags=["post"])
api_router.include_router(story_router, prefix="/story", tags=["story"])
api_router.include_router(user_router, prefix="/user", tags=["user"])