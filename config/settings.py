from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",env_prefix="DEV_")
    stripe_api_key: str
    salesforce_token: str
    database_url: str
    dummy_json_url:str

settings: Settings = Settings()
