import logging

from fastapi import APIRouter
from llm_chatbot_api.api.schemas import AddChatRequest, GetChatsRequest, GetChatsResponse
from llm_chatbot_api.db.crud import get_user_chats, create_chat
from llm_chatbot_api.db.database import get_session
from llm_chatbot_api.db import models
from llm_chatbot_api.api import schemas
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/add_chat", operation_id="ADD-CHAT")
def add_chat(request: AddChatRequest):
    db: Session = get_session()
    logger.info(f"Creating a chat for user {request.user_id}")
    db_chat = create_chat(db, user_id=request.user_id, name=request.chat_name)
    return {"message": "Chat added successfully."}

@router.post("/get_chats", operation_id="GET-CHATS")
def read_user_chats(request: GetChatsRequest) -> GetChatsResponse:
    db: Session = get_session()
    logger.info(f"Getting chats for user {request.user_id}")
    db_chats = get_user_chats(db, request.user_id)
    chats = [schemas.Chat(user_id=db_chat.user_id, chat_id=db_chat.id, chat_name=db_chat.name) for db_chat in db_chats]
    return GetChatsResponse(user_id=request.user_id, chats=chats)
