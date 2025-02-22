from typing import List, Optional, Sequence
from instaclone.database.connection import SESSION
from sqlalchemy.sql import select

from instaclone.app.medium.models import Medium
from instaclone.database.annotation import transactional
from instaclone.app.medium.errors import FailedToDelete, FailedToSave


class MediumStore:
    async def get_medium_by_id(self, image_id: int) -> Optional[Medium]:
        return await SESSION.scalar(select(Medium).where(Medium.image_id == image_id))

    async def get_media_by_post(self, post_id: int) -> Sequence[Medium]:
        result = await SESSION.scalars(select(Medium).where(Medium.post_id == post_id))
        return result.all()
    
    @transactional
    async def add_medium(self,
                         post_id: int | None,
                        #  story_id: int | None,
                         file_name: str, 
                         url: str
                         ) -> Medium:
        medium = Medium(file_name=file_name, 
                        url=url, post_id=post_id)
        try:
            SESSION.add(medium)
            await SESSION.commit()
            return medium
        except:
            await SESSION.rollback()
            raise FailedToSave()

    @transactional
    async def delete_medium(self, image_id: int) -> None:
        medium = await self.get_medium_by_id(image_id)
        try:
            if medium:
                await SESSION.delete(medium)
                await SESSION.commit()
        except Exception as e:
            await SESSION.rollback()
            raise FailedToDelete()

