import logging.config
import os

from omegaconf import OmegaConf

from llm_chatbot_api.db.models import Message

# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)

# Apply the logging configuration
logging.config.dictConfig(logging_config)

# Configure logging
logger = logging.getLogger(__name__)

class FireworksLLM:
    def __init__(self, model_name: str, system_prompt: str):
        import fireworks.client
        FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
        if FIREWORKS_API_KEY is None:
            logger.error("FIREWORKS_API_KEY is not set in the environment variables.")
            raise ValueError("FIREWORKS_API_KEY is not set in the environment variables.")
        fireworks.client.api_key = FIREWORKS_API_KEY
        self.client = fireworks.client
        self.model_name = model_name
        self.system_prompt = system_prompt

    def run(self, chathistory: list[Message]):
        """Run the LLM with the given prompt text or file path."""
        completion = self.client.ChatCompletion.create(
            model=self.model_name,
            messages=[
                chathistory
            ],
            max_tokens=3200,
            temperature=0.5,
            presence_penalty=0,
            frequency_penalty=0,
            top_p=1,
            top_k=40
        )
        return completion.choices[0].message.content