from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = Field(default="Translate AI", env="APP_NAME")
    app_version: str = Field(default="0.1.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")

    cohere_api_key: str = Field(env="COHERE_API_KEY")
    groq_api_key: str = Field(env="GROQ_API_KEY")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

# Singleton instance
settings = Settings()