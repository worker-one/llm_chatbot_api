import logging

from fastapi import APIRouter
from llm_chatbot_api.api import schemas
from llm_chatbot_api.api.schemas import AddChatRequest, GetChatsResponse
from llm_chatbot_api.db import crud

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chats")
def add_chat(request: AddChatRequest):
    logger.info(f"Creating a chat for user {request.user_id}")

    # check if user exists
    db_user = crud.read_user(request.user_id)
    if db_user is None:
        return {"message": f"User with id {request.user_id} does not exist."}

    crud.create_chat(user_id=request.user_id, name=request.chat_name)
    return {"message": "Chat added successfully."}

@router.get("/chats/{user_id}")
def read_user_chats(user_id) -> GetChatsResponse:
    logger.info(f"Getting chats for user {user_id}")
    db_chats = crud.get_user_chats(user_id)
    chats = [schemas.Chat(user_id=db_chat.user_id, chat_id=db_chat.id, chat_name=db_chat.name) for db_chat in db_chats]
    return GetChatsResponse(user_id=user_id, chats=chats)

@router.delete("/chats/{user_id}/{chat_id}")
def delete_chat(user_id: int, chat_id: int):
    logger.info(f"Deleting chat {chat_id} for user {user_id}")
    try:
        crud.delete_chat(user_id=user_id, chat_id=chat_id)
        return {"message": "Chat deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting chat: {e}")
        raise e
