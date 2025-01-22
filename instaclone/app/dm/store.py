from typing import Sequence, Optional, List
from sqlalchemy.sql import select, delete, or_

from instaclone.database.connection import SESSION
from instaclone.app.dm.models import Message
from instaclone.app.dm.errors import MessageNotFoundError, MessagePermissionError

class DMStore:
    async def get_message_from_id(self, message_id: int) -> Message:
        message = await SESSION.scalar(select(Message).where(Message.message_id == message_id))
        if not message:
            raise MessageNotFoundError()
        return message
    
    async def get_sent_messages(self, user_id: int) -> Sequence["Message"]:
        result = await SESSION.scalars(select(Message).where(Message.sender_id == user_id))
        return result.all()
    
    async def get_received_messages(self, user_id: int) -> Sequence["Message"]:
        result = await SESSION.scalars(select(Message).where(Message.receiver_id == user_id))
        return result.all()

    async def create_message(self, sender_id: int, receiver_id: int, text: str) -> Optional[Message]:
        message = Message(sender_id=sender_id, receiver_id=receiver_id, text=text)
        try:
            SESSION.add(message)
            await SESSION.commit()
            return message
        except:
            await SESSION.rollback()

    async def delete_message(self, user_id: int, message_id: int) -> None:
        message = await self.get_message_from_id(message_id)
        if not message:
            raise MessageNotFoundError()
        if message.sender_id != user_id:
            raise MessagePermissionError()
        
        query = delete(Message).where(Message.message_id == message_id)
        try:
            await SESSION.execute(query)
            await SESSION.commit()
        except:
            await SESSION.rollback()