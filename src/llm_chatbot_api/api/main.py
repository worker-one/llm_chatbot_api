import logging
import uvicorn
from fastapi import FastAPI
from omegaconf import OmegaConf

from llm_chatbot_api.api.routes import chats, llm, users
from llm_chatbot_api.db.database import create_tables

# Load logging configuration with OmegaConf
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_path: str) -> FastAPI:
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
    app.include_router(llm.router)

    return app


if __name__ == "__main__":
    config_path = "src/llm_chatbot_api/conf/config.yaml"
    config = OmegaConf.load(config_path)
    create_tables()
    app = create_app(config_path)
    logger.info("Starting the API server...")
    uvicorn.run(app, host=config.api.host, port=config.api.port, log_level="info")
    logger.info("API server stopped.")
