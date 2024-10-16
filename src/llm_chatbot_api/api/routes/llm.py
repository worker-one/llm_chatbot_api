import io
import logging
from datetime import datetime

from fastapi import APIRouter, File, Form, UploadFile
from hydra.utils import instantiate
from llm_chatbot_api.api.schemas import ModelConfig, QueryModelResponse
from llm_chatbot_api.core.file import TextFileParser
from llm_chatbot_api.core.llm import LLM
from llm_chatbot_api.db import crud
from llm_chatbot_api.utils.exceptions import (
    ChatDoesNotExist,
    MessageIsEmpty,
    UnsupportedFileTypeException,
    UserDoesNotExist,
)
from omegaconf import OmegaConf
from PIL import Image

# Load logging configuration with OmegaConf
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = OmegaConf.load("./src/llm_chatbot_api/conf/config.yaml")
model_config = instantiate(config.llm.config.default)
llm = LLM(model_config)

logger.info(f"Model configuration: {model_config}")

router = APIRouter()
# Initialize TextFileParser with appropriate parameters
text_file_parser = TextFileParser(max_file_size_mb=10, allowed_file_types={"txt", "doc", "docx", "pdf"})

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
async def query(
    user_id: str = Form(...),
    chat_id: str = Form(...),
    user_message: str = Form(None),
    config: ModelConfig = Form(None),
    files: list[UploadFile] = File(None)
) -> QueryModelResponse:
    # check if user exists
    db_user = crud.read_user(user_id)
    if db_user is None:
        raise UserDoesNotExist()

    # check if chat exists
    db_chat = crud.get_chat(chat_id, user_id)
    if db_chat is None:
        raise ChatDoesNotExist()

    if not user_message and not files:
        raise MessageIsEmpty()

    logger.info(f"User {user_id} sent message: `{user_message}` in chat {chat_id}")

    # Process the files if uploaded
    images = []
    texts = []
    if files:
        for file in files:
            try:
                file_extension = file.filename.rsplit(".", 1)[1].lower()
                if file_extension in {"jpg", "jpeg", "png", "gif"}:
                    image_bytes = await file.read()  # Read the file contents
                    image = Image.open(io.BytesIO(image_bytes))  # Convert to PIL Image
                    images.append(image)
                    logger.info(f"Received image {file.filename} from user {user_id}")
                elif file_extension in {"pdf", "doc", "docx", "txt"}:
                    uploaded_file = UploadFile(
                        filename=file.filename,
                        file=io.BytesIO(await file.read()),
                        size=file.size,
                        headers={"content-type": file.content_type}
                    )
                    text_content = text_file_parser.extract_content(uploaded_file)
                    texts.append(f"Document {file.filename}: {text_content}")
                    logger.info(f"Received text file {file.filename} from user {user_id}")
                else:
                    raise UnsupportedFileTypeException(f"Unsupported file type: {file_extension}")
            except Exception as e:
                logger.error(f"Error processing file {file.filename}: {e}")
                raise e

    user_message += "\n".join(texts)

    # TODO
    if len(user_message) > 10000:
        user_message = user_message[:10000]

    # add the message to the chat history if it exists
    crud.create_message(chat_id, "user", content=user_message, timestamp=datetime.now())

    # get the chat history
    chat_history = crud.get_chat_history(chat_id)

    # invoke the model with chat history, texts, and optionally with the images
    try:
        response = llm.invoke(chat_history, config, images=images)
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
