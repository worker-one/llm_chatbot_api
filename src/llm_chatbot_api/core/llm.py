from langchain_core.messages import AIMessage, HumanMessage
from langchain_fireworks import ChatFireworks
from langchain_openai import ChatOpenAI
from llm_chatbot_api.api.schemas import ModelConfig, ModelResponse


class LLM:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.clients = {
            "openai": ChatOpenAI,
            "fireworksai": ChatFireworks
        }

    def update_config(self, config: ModelConfig) -> None:
        """
        Updates the current configuration of the model with the provided configuration.

        Args:
            config (ModelConfig): An instance of ModelConfig containing the new configuration values.
        """
        for attr in ['provider', 'model_name', 'max_tokens', 'chat_history_limit', 'temperature']:
            if getattr(config, attr) is not None:
                self.config.__setattr__(attr, getattr(config, attr))

    def invoke(self, chat_history: list[str], config: ModelConfig = None) -> ModelResponse:
        """
        Invokes the language model with the given chat history and configuration.
        Args:
            chat_history (list[str]): A list of chat messages.
            config (ModelConfig, optional): The configuration for the model. If not provided, 
                                            the instance's default configuration will be used.
        Returns:
            ModelResponse: The response from the language model.
        Raises:
            ValueError: If no configuration is provided and the instance's default configuration is None.
            ValueError: If the specified provider is not available in the clients.
        """
        if config is None and self.config is not None:
            config = self.config
        else:
            raise ValueError("Model configuration is required")
        provider = config.provider
        if provider not in self.clients:
            raise ValueError(f"Invalid provider: {provider}. Available providers: {', '.join(self.clients.keys())}")
        client = self.clients[provider](
            model_name=config.model_name,
            max_tokens=config.max_tokens,
            temperature=config.temperature
        )

        chat_history = chat_history[-config.chat_history_limit:]
        role_message_map = {"user": HumanMessage, "assistant": AIMessage}
        messages = [
            role_message_map[message.role](content=[{"type": "text", "text": message.content}])
            for message in chat_history if message.role in role_message_map
        ]
        for message in messages:
            print(type(message))
        response = client.invoke(messages)
        return ModelResponse(response_content=response.content, config=config)

