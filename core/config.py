import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # WhatsApp Meta API Configuration
    WHATSAPP_TOKEN: str = "your_whatsapp_token_here"
    VERIFY_TOKEN: str = "your_custom_verify_token_here"
    PHONE_NUMBER_ID: str = "your_phone_number_id_here"
    USE_LLM: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
