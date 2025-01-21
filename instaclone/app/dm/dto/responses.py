from typing import cast
from datetime import datetime
from pydantic import BaseModel

from instaclone.app.dm.models import Message

class MessageDetailResponse(BaseModel):
    message_id: int
    sender_id: int
    receiver_id: int
    text: str
    creation_date: datetime

    @staticmethod
    def from_message(message: Message) -> "MessageDetailResponse":
        return MessageDetailResponse(
            message_id=message.message_id,
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            text=message.text,
            creation_date=cast(datetime, message.creation_date)
        )