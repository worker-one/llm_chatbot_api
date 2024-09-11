import logging
from datetime import datetime

from fastapi import APIRouter
from omegaconf import OmegaConf
from hydra.utils import instantiate



from llm_chatbot_api.api.schemas import QueryChatbotRequest, QueryChatbotResponse, ModelInfoResponse, SetModelRequest
from llm_chatbot_api.db import crud
from llm_chatbot_api.utils.exceptions import UserDoesNotExist, ChatDoesNotExist, MessageIsEmpty, MessageIsTooLong

# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("./src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

config = OmegaConf.load("./src/llm_chatbot_api/conf/config.yaml")

if config.llm.provider == "openai":
    llm = instantiate(config.llm.clients.openai)
    logger.info(f"Connected to the model `{llm.model_name}` with OpenAI")
elif config.llm.provider == "fireworksai":
    llm = instantiate(config.llm.clients.fireworksai)
    logger.info(f"Connected to the model `{llm.model_name}` with FireworksAI")
else:
    raise ValueError(f"Invalid LLM provider: {config.llm.provider}")

router = APIRouter()

MAX_MESSAGE_LENGTH = 2000

@router.get("/info")
def info() -> ModelInfoResponse:
    return ModelInfoResponse(
        model_name=llm.model_name,
        provider=llm.provider,
        max_tokens=llm.max_tokens,
        chat_history_limit=llm.chat_history_limit
    )

@router.post("/set_model")
def set_model(request: SetModelRequest):
    global llm
    llm.model_name = request.model_name if request.model_name is not None else llm.model_name
    llm.max_tokens = request.max_tokens if request.max_tokens is not None else llm.max_tokens
    llm.chat_history_limit = request.chat_history_limit if request.chat_history_limit is not None else llm.chat_history_limit
    
    # check that the model is valid
    try:
        llm.invoke([])
    except Exception as e:
        llm = instantiate(config.llm.clients.openai)
        return {
            "status": "error",
            "message": "Configuration not valid."
            f"Resetting to default model `{llm.model_name}`"
        }
 
    return {"status": "success", "message": "Model updated successfully"}

@router.post("/query")
def query(request: QueryChatbotRequest) -> QueryChatbotResponse:
    user_id = request.user_id
    chat_id = request.chat_id
    user_message = request.user_message

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
    ai_message = llm.invoke(chat_history)

    logger.info(f"AI responded with message: `{ai_message}`")

    try:
        # add the response to the chat history
        crud.create_message(chat_id, "assistant", content=ai_message, timestamp=datetime.now())
    except Exception as e:
        logger.error(f"Error adding AI message to chat history: {e}")
        raise e
    response = QueryChatbotResponse(user_id=user_id, chat_id=chat_id, ai_message=ai_message)
    return response
