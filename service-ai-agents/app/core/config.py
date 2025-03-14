from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class Settings(BaseSettings):
    LLM_API_KEY: str
    LLM_URL: str
    LLM_MODEL: str
    LLM_API_VERSION: str
    DIFY_BACKEND: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
