import logging
import uvicorn
from fastapi import FastAPI
from omegaconf import OmegaConf

from llm_chatbot_api.api.endpoint import *


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def create_app(config_path: str = "src/text_classification/conf/config.yaml") -> FastAPI:
    """
    Create a FastAPI application with the specified configuration.
    Args:
        config_path: The path to the configuration file in yaml format

    Returns:
        FastAPI: The FastAPI application instance.
    """
    config = OmegaConf.load(config_path)

    app = FastAPI(title=config.api.title, description=config.api.description, version=config.api.version)

    app.include_router(chats.router)
    app.include_router(users.router)
    app.include_router(invoke.router)

    return app


if __name__ == "__main__":
    config_path = "src/llm_chatbot_api/conf/config.yaml"
    config = OmegaConf.load(config_path)
    app = create_app(config_path)
    logger.info("Starting the API server...")
    uvicorn.run(app, host=config.api.host, port=config.api.port)
    logger.info("API server stopped.")
