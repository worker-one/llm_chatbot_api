from pydantic import BaseModel

from llm_chatbot_api.src.llm_chatbot_api.db.schema import Chat


class InvokeChatbotRequest(BaseModel):
    user_id: str
    chat_id: str
    user_message: str

class InvokeChatbotResponse(BaseModel):
    user_id: str
    chat_id: str
    llm_message: str

class ChatsRequest(BaseModel):
    user_id: str

class ChatsResponse(BaseModel):
    chats: list[Chat]
