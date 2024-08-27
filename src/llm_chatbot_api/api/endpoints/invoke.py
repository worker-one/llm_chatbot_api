from fastapi import APIRouter
from sqlalchemy.orm import Session

from llm_chatbot_api.db import crud, models
from llm_chatbot_api.db.database import get_session
from llm_chatbot_api.core.llm import FireworksLLM
from llm_chatbot_api.api.schemas import InvokeChatbotRequest, InvokeChatbotResponse


llm = FireworksLLM()

router = APIRouter()

@router.get("/invoke/{user_id}")
def invoke(request: InvokeChatbotRequest) -> InvokeChatbotResponse:
    user_id = request.user_id
    chat_id = request.chat_id
    message = request.message

    db: Session = get_session()

    # add the message to the chat history
    crud.create_message(db, chat_id, "user", message, None)

    # get the chat history
    chathistory = crud.get_chat_history(db, user_id, chat_id)
    response = llm.invoke(chathistory, message)
    return response