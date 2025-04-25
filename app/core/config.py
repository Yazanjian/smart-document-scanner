from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

    project_name: str = "Intelligent-Documents-Scanner"
    environment: str = "dev"
    default_language: str = "en"
    enable_translation: bool = False
    model_name: str
    model_temperature: int = 0
    openai_api_key: str


app_settings = Settings()
