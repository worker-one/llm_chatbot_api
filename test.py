from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
from llm_chatbot_api.api.schemas import ImageModelConfig

class ImageModel:
    def __init__(self, config: ImageModelConfig):
        self.config = config
        if self.config.provider == "OpenAI":
            self.client = OpenAI()
        else:
            raise ValueError(f"Invalid provider: {self.config.provider}")

    def update_config(self, config: ImageModelConfig) -> None:
        for attr in ['model_name', 'n', 'quality', 'size']:
            if getattr(config, attr) is not None:
                self.config.__setattr__(attr, getattr(config, attr))

    def generate_image(self, prompt: str) -> str:
        image_url = self.client.images.generate(
            model=self.config.model_name,
            prompt=prompt,
            size=self.config.size,
            quality=self.config.quality,
            n=self.config.n
        )
        return image_url



load_dotenv(find_dotenv(usecwd=True))
model_config = ImageModelConfig(
    model_name="dall-e-3",
    provider="OpenAI"
)
print(model_config)
model = ImageModel(model_config)

desc = "A beautiful sunset over the ocean"
print(model.generate_image(desc))