# app/config.py
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    api_base_url: str = "https://qa.sirrus.ai/api/ilead-service/v1"
    bearer_token: str
    client_id: str = "TCG-WEB-APP"
    group_by: str = "leadStatus"
    map_related_entities: str = "true"
    limit: str = "9999999999"
    
    # Gemini AI settings
    gemini_api_key: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()