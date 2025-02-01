from sqlalchemy import text
from starlette.middleware.base import BaseHTTPMiddleware

from instaclone.database.connection import SESSION, reset_session, start_default_session


class DefaultSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        tokens = start_default_session()
        await SESSION.execute(text("START TRANSACTION READ ONLY"))
        try:
            response = await call_next(request)
            await SESSION.commit()
        except Exception as e:
            raise e
        finally:
            await SESSION.close()
            reset_session(tokens)
        return response