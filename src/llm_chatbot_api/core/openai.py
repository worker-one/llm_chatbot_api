import os
import requests
import logging.config

from omegaconf import OmegaConf

from llm_chatbot_api.api.schemas import Message

logging_config = OmegaConf.to_container(OmegaConf.load("./src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


class OpenAI:
    def __init__(
            self,
            model_name: str,
            prompt_template: str,
            max_tokens: int = 400,
            chat_history_limit: int = 10,
            temperature: float = 0.7
    ):
        self.base_url = "https://api.openai.com/v1/chat/completions"
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if OPENAI_API_KEY is None:
            logger.error("OPENAI_API_KEY is not set in the environment variables.")
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        self.model_name = model_name
        self.provider = "openai"
        self.prompt_template = prompt_template
        self.max_tokens = max_tokens
        self.chat_history_limit = chat_history_limit
        self.temperature = temperature

    def invoke(self, chat_history: list[Message]):
        """Run the LLM model with the given query."""

        #chat_history = chat_history[-self.chat_history_limit:]
        messages = [{"role": message.role, "content": message.content} for message in chat_history]

        for message in messages:
            print(message)

        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }


        response = requests.post(self.base_url, headers=self.headers, json=payload)

        # Check if the response code is not 200
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]