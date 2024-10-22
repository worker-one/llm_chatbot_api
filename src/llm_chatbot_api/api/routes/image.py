import io
import logging
from datetime import datetime

from fastapi import APIRouter, File, Form, UploadFile
from hydra.utils import instantiate
from llm_chatbot_api.api.schemas import ImageModelConfig, QueryImageModelResponse
from llm_chatbot_api.core.file import TextFileParser
from llm_chatbot_api.core.image_model import ImageModel
from llm_chatbot_api.db import crud
from llm_chatbot_api.utils.exceptions import (
    MessageIsEmpty,
    UnsupportedFileTypeException,
    UserDoesNotExist,
)
from omegaconf import OmegaConf

# Load logging configuration with OmegaConf
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = OmegaConf.load("./src/llm_chatbot_api/conf/config.yaml")
model_config = instantiate(config.image_model.config.default)
image_model = ImageModel(model_config)

logger.info(f"Image Model configuration: {model_config}")

router = APIRouter()

text_file_parser = TextFileParser(max_file_size_mb=10, allowed_file_types={"txt", "doc", "docx", "pdf"})


@router.get("/config")
def get_image_model_config() -> ImageModelConfig:
    return image_model.config

@router.post("/config")
def update_image_model_config(request: ImageModelConfig):
    global image_model
    try:
        image_model.update_config(request)
        return {"status": "success", "message": "Image model updated successfully"}
    except Exception as e:
        logger.error(f"Error updating image model: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/generate")
async def generate_image(
    user_id: str = Form(...),
    user_message: str = Form(None),
    config: ImageModelConfig = Form(None),
    files: list[UploadFile] = File(None)
) -> QueryImageModelResponse:
    # check if user exists
    db_user = crud.read_user(user_id)
    if db_user is None:
        raise UserDoesNotExist()

    if not user_message and not files:
        raise MessageIsEmpty()

    logger.info(f"User {user_id} requested image generation with description: `{user_message}`")

    # Process the files if uploaded
    texts = []
    if files:
        for file in files:
            try:
                file_extension = file.filename.rsplit(".", 1)[1].lower()
                if file_extension in {"pdf", "doc", "docx", "txt"}:
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

    if texts:
        user_message += "\n".join(texts)

    # invoke the model with chat history and description
    try:
        response = image_model.generate_image(user_message)
    except Exception as e:
        logger.error(f"Error invoking image model: {e}")
        raise e

    response = QueryImageModelResponse(
        user_id=user_id,
        prompt=user_message,
        model_response=response
    )
    return response
