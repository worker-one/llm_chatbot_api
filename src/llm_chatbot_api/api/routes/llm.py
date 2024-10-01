import logging
from datetime import datetime

from fastapi import APIRouter
from hydra.utils import instantiate
from llm_chatbot_api.api.schemas import ModelConfig, QueryModelRequest, QueryModelResponse
from llm_chatbot_api.core.llm import LLM
from llm_chatbot_api.db import crud
from llm_chatbot_api.utils.exceptions import ChatDoesNotExist, MessageIsEmpty, MessageIsTooLong, UserDoesNotExist
from omegaconf import OmegaConf

# Load logging configuration with OmegaConf
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = OmegaConf.load("./src/llm_chatbot_api/conf/config.yaml")
model_config = instantiate(config.llm.config.default)
llm = LLM(model_config)

logger.info(f"Model configuration: {model_config}")

router = APIRouter()

MAX_MESSAGE_LENGTH = 2000

@router.get("/model/config")
def get_model_config() -> ModelConfig:
    return llm.config

@router.post("/model/config")
def update_model_config(request: ModelConfig):
    global llm
    try:
        llm.update_config(request)
        return {"status": "success", "message": "Model updated successfully"}
    except Exception as e:
        logger.error(f"Error updating model: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/model/query")
def query(request: QueryModelRequest) -> QueryModelResponse:
    user_id = request.user_id
    chat_id = request.chat_id
    user_message = request.user_message
    config = request.config

    # check if user exists
    db_user = crud.read_user(user_id)
    if db_user is None:
        raise UserDoesNotExist()

    # check if chat exists
    db_chat = crud.get_chat(chat_id, user_id)
    if db_chat is None:
        raise ChatDoesNotExist()

    if not user_message:
        raise MessageIsEmpty()

    if len(user_message) > MAX_MESSAGE_LENGTH:
        raise MessageIsTooLong()

    logger.info(f"User {user_id} sent message: `{user_message}` in chat {chat_id}")

    # add the message to the chat history
    crud.create_message(chat_id, "user", content=user_message, timestamp=datetime.now())

    # get the chat history
    chat_history = crud.get_chat_history(chat_id)

    # invoke the model
    try:
        response = llm.invoke(chat_history, config)
        ai_message = response.response_content
    except Exception as e:
        logger.error(f"Error invoking model: {e}")
        raise e

    logger.info(f"AI responded with message: `{ai_message}`")

    try:
        # add the response to the chat history
        crud.create_message(chat_id, "assistant", content=ai_message, timestamp=datetime.now())
    except Exception as e:
        logger.error(f"Error adding AI message to chat history: {e}")
        raise e
    response = QueryModelResponse(
        user_id=user_id,
        chat_id=chat_id,
        model_response=response
    )
    return response
