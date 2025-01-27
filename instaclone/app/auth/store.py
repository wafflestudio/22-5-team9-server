from sqlalchemy.future import select
from datetime import datetime
from instaclone.app.user.models import User
from instaclone.database.connection import SESSION
from sqlalchemy.exc import SQLAlchemyError
from instaclone.common.errors import CommentServerError

async def get_or_create_user_from_google(user_info: dict):
    try:
        # User DB - email 기반 사용자 정보 조회
        async with SESSION() as session:
            stmt = select(User).filter_by(email=user_info["email"])
            result = await session.execute(stmt)
            user = result.scalars().first()

            # 유저가 새로 생성된 경우
            if not user:
                user = User(
                    username=user_info.get("name"),
                    email=user_info.get("email"),
                    full_name=user_info.get("name"),
                    password="default",
                    creation_date=datetime.today().date(),
                    profile_image=user_info.get("picture"),
                    social=True
                )
                session.add(user)
                await session.commit()
                return {
                    "user": user,
                    "is_created": True
                }

            # 유저가 이미 있는 경우
            return {
                "user": user,
                "is_created": False
            }
        
    except SQLAlchemyError as e:
        # 예외가 발생하면 롤백 처리하고, 커스텀 예외 던지기
        await SESSION.rollback()
        raise CommentServerError(f"Failed to create or retrieve user: {str(e)}", e) from e