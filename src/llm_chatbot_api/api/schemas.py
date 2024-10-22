from datetime import datetime
from logging import config
from typing import Literal, Optional

from prompt_toolkit import prompt

from pydantic import BaseModel, confloat, conint


class Message(BaseModel):
    chat_id: str
    role: str
    content: str
    timestemp: datetime

class User(BaseModel):
    id: int
    name: str

class Chat(BaseModel):
    user_id: int
    chat_id: int
    chat_name: str

class AddUserRequest(BaseModel):
    user: User

class AddChatRequest(BaseModel):
    user_id: int
    chat_name: str

class DeleteChatRequest(BaseModel):
    user_id: int
    chat_id: int

class DeleteChatResponse(BaseModel):
    chat_id: int

class GetChatsRequest(BaseModel):
    user_id: int

class GetChatsResponse(BaseModel):
    chats: list[Chat]

class ModelConfig(BaseModel):
    model_name: Optional[str] = None
    provider: Optional[str] = None
    max_tokens: Optional[conint(ge=0)] = None
    chat_history_limit: Optional[conint(ge=0)] = None
    temperature: Optional[confloat(ge=0.0)] = None

class ImageModelConfig(BaseModel):
    model_name: Optional[str] = "dall-e-2"  # The name of the model to use for image generation
    provider: Literal["OpenAI"] = "OpenAI"  # The provider of the model
    n: Optional[conint(ge=0)] = 1  # Number of images to generate
    quality: Literal["standard", "hd"] = "standard"  # The quality of the generated images
    size: Optional[str] = "1024x1024"  # The size of the generated images

class ModelResponse(BaseModel):
    response_content: str
    config: ModelConfig

class ImageModelResponse(BaseModel):
    response_content: list[dict[str, str]]
    config: ImageModelConfig

class QueryModelRequest(BaseModel):
    user_id: conint(ge=0)
    chat_id: conint(ge=0)
    user_message: str
    config: Optional[ModelConfig] = None

class QueryModelResponse(BaseModel):
    user_id: conint(ge=0)
    chat_id: conint(ge=0)
    model_response: ModelResponse

class QueryImageModelResponse(BaseModel):
    user_id: conint(ge=0)
    prompt: str
    model_response: ImageModelResponse
