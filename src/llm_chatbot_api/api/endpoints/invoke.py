import logging
from datetime import datetime

from fastapi import APIRouter
from llm_chatbot_api.api.schemas import InvokeChatbotRequest, InvokeChatbotResponse
from llm_chatbot_api.core.llm import FireworksLLM
from llm_chatbot_api.db import crud, models
from llm_chatbot_api.db.database import get_session
from omegaconf import OmegaConf
from sqlalchemy.orm import Session

# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("./src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

config = OmegaConf.load("./src/llm_chatbot_api/conf/config.yaml")
llm = FireworksLLM(
    config.llm.model_name,
    config.llm.system_prompt,
    config.llm.max_tokens
)

router = APIRouter()

@router.post("/invoke", operation_id="INVOKE-LLM")
def invoke(request: InvokeChatbotRequest) -> InvokeChatbotResponse:
    user_id = request.user_id
    chat_id = request.chat_id
    user_message = request.user_message

    logger.info(f"User {user_id} sent message: `{user_message}` in chat {chat_id}")

    db: Session = get_session()

    # add the message to the chat history
    crud.create_message(db, chat_id, "user", content=user_message, timestamp=datetime.now())

    # get the chat history
    chat_history = crud.get_chat_history(db, user_id, chat_id)
    ai_message = llm.invoke(chat_history)

    logger.info(f"AI responded with message: `{ai_message}`")

    try:
        # add the response to the chat history
        crud.create_message(db, chat_id, "assistant", content=ai_message, timestamp=datetime.now())
    except Exception as e:
        logger.error(f"Error adding AI message to chat history: {e}")
        raise e
    response = InvokeChatbotResponse(user_id=user_id, chat_id=chat_id, ai_message=ai_message)
    return response
