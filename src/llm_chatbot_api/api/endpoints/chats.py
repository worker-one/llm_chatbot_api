import logging

from fastapi import APIRouter
from llm_chatbot_api.api.schemas import ChatsRequest, ChatsResponse
from llm_chatbot_api.db.crud import get_user_chats
from llm_chatbot_api.db.database import get_session
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
@router.get("/chats")
def read_user_chats(request: ChatsRequest) -> ChatsResponse:
    user_id = request.user_id
    db: Session = get_session()
    logger.info(f"Getting chats for user {user_id}")
    chats = get_user_chats(db, user_id)
    return chats
