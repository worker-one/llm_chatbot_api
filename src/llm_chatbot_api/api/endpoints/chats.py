import logging

from fastapi import APIRouter
from llm_chatbot_api.api import schemas
from llm_chatbot_api.api.schemas import AddChatRequest, DeleteChatRequest, GetChatsRequest, GetChatsResponse
from llm_chatbot_api.db import crud
from llm_chatbot_api.db.database import get_session
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/add_chat", operation_id="ADD-CHAT")
def add_chat(request: AddChatRequest):
    db: Session = get_session()
    logger.info(f"Creating a chat for user {request.user_id}")
    crud.create_chat(db, user_id=request.user_id, name=request.chat_name)
    return {"message": "Chat added successfully."}

@router.post("/get_chats", operation_id="GET-CHATS")
def read_user_chats(request: GetChatsRequest) -> GetChatsResponse:
    db: Session = get_session()
    logger.info(f"Getting chats for user {request.user_id}")
    db_chats = crud.get_user_chats(db, request.user_id)
    chats = [schemas.Chat(user_id=db_chat.user_id, chat_id=db_chat.id, chat_name=db_chat.name) for db_chat in db_chats]
    return GetChatsResponse(user_id=request.user_id, chats=chats)

@router.post("/delete_chat", operation_id="DELETE-CHAT")
def delete_chat(request: DeleteChatRequest):
    db: Session = get_session()
    logger.info(f"Deleting chat {request.chat_id} for user {request.user_id}")
    try:
        crud.delete_chat(db, user_id=request.user_id, chat_id=request.chat_id)
        return {"message": "Chat deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting chat: {e}")
        raise e
