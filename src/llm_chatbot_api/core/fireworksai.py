import logging.config
import os

from omegaconf import OmegaConf

from llm_chatbot_api.api.schemas import Message

# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

class FireworksLLM:
    def __init__(
            self,
            model_name: str,
            system_prompt: str,
            max_tokens: int = 500,
            chat_history_limit: int = 10
        ):
        import fireworks.client
        FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
        if FIREWORKS_API_KEY is None:
            logger.error("FIREWORKS_API_KEY is not set in the environment variables.")
            raise ValueError("FIREWORKS_API_KEY is not set in the environment variables.")
        fireworks.client.api_key = FIREWORKS_API_KEY
        self.client = fireworks.client
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.chat_history_limit = chat_history_limit

    def invoke(self, chat_history: list[Message]):
        """Run the LLM with the given prompt text or file path.
        
        Args:
            chat_history: List of messages in the chat history.

        Returns:
            str: The response from the LLM.

        Raises:
            Exception: If the LLM invocation fails.

        """
        chat_history = chat_history[-self.chat_history_limit:]
        messages = [{"role": message.role, "content": message.content} for message in chat_history]
        try:
            completion = self.client.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.2,
                presence_penalty=0,
                frequency_penalty=0,
                top_p=1,
                top_k=40
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error invoking Fireworks LLM: {e}")
            raise e
