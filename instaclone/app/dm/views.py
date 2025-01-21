import json
from typing import List, Annotated
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from starlette.status import HTTP_200_OK

from instaclone.app.user.models import User
from instaclone.app.user.views import login_with_header
from instaclone.app.dm.manager import DMManager
from instaclone.app.dm.service import DMService
from instaclone.app.dm.dto.responses import MessageDetailResponse
from instaclone.app.auth.utils import ws_login_with_header

dm_router = APIRouter()
dm_manager = DMManager()

@dm_router.websocket("/")
async def dm_management(
    websocket: WebSocket,
    dm_service: Annotated[DMService, Depends()],    
    user: Annotated[User, Depends(ws_login_with_header)]
):  
    await dm_manager.connect(user.user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            receiver_id = message_data["receiver_id"]
            text = message_data["text"]
            await dm_manager.send_personal_message(text, user.user_id, int(receiver_id))
            await dm_service.create_message(user.user_id, receiver_id, text)
    except WebSocketDisconnect:
        dm_manager.disconnect(user.user_id)

@dm_router.get("/message/{message_id}", status_code=HTTP_200_OK)
async def get_message(
    dm_service: Annotated[DMService, Depends()],
    message_id: int
) -> MessageDetailResponse:
    message = await dm_service.get_message(message_id)
    return MessageDetailResponse.from_message(message)

@dm_router.get("/sent", status_code=HTTP_200_OK)
async def get_sent_messages(
    dm_service: Annotated[DMService, Depends()],
    user: Annotated[User, Depends(login_with_header)]
) -> List[MessageDetailResponse]:
    sent_messages = await dm_service.get_sent_messages(user.user_id)
    return [MessageDetailResponse.from_message(m) for m in sent_messages]

@dm_router.get("/received", status_code=HTTP_200_OK)
async def get_received_messages(
    dm_service: Annotated[DMService, Depends()],
    user: Annotated[User, Depends(login_with_header)]
) -> List[MessageDetailResponse]:
    received_messages = await dm_service.get_received_messages(user.user_id)
    return [MessageDetailResponse.from_message(m) for m in received_messages]

@dm_router.delete("/{message_id}", status_code=HTTP_200_OK)
async def delete_message(
    dm_service: Annotated[DMService, Depends()],
    message_id: int,
    user: Annotated[User, Depends(login_with_header)]
) -> str:
    await dm_service.delete_message(user.user_id, message_id)
    return "SUCCESS"