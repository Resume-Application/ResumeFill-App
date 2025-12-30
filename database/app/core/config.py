from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

class Settings(BaseSettings):
    API_V1_STR: str = ""
    PROJECT_NAME: str = "FastAutofill Backend"
    PROJECT_URL : str = "https://autofill.com"
    
    # Security
    SECRET_KEY: str = "TEMPORARY" 
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
