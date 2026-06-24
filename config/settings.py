from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",env_prefix="DEV_")
    stripe_api_key: str
    database_url: str
    dummy_json_url:str
    salesforce_endpoint : str
    salesforce_access_token : str
    zendesk_endpoint : str
    zendesk_access_token : str
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_s3_bucket_name: str = ""

settings: Settings = Settings()
