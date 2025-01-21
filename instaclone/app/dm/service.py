from typing import Annotated, List, Sequence, Optional
from fastapi import Depends

from instaclone.app.dm.store import DMStore
from instaclone.app.dm.models import Message

class DMService:
    def __init__(self, dm_store: Annotated[DMStore, Depends()]) -> None:
        self.dm_store = dm_store

    async def get_message(self, message_id: int) -> Message:
        return await self.dm_store.get_message_from_id(message_id)
    
    async def create_message(self, sender_id: int, receiver_id: int, text: str) -> Optional["Message"]:
        message = await self.dm_store.create_message(sender_id, receiver_id, text)
        return message
    
    async def get_sent_messages(self, user_id: int) -> Sequence["Message"]:
        sent_messages = await self.dm_store.get_sent_messages(user_id)
        return sent_messages
    
    async def get_received_messages(self, user_id: int) -> Sequence["Message"]:
        received_messages = await self.dm_store.get_received_messages(user_id)
        return received_messages
    
    async def delete_message(self, user_id: int, message_id: int) -> None:
        await self.dm_store.delete_message(user_id, message_id)