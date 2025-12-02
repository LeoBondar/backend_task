from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class SrvSettings(BaseSettings):
    app_name: str = "Lead Distribution CRM"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SRV_")


class DatabaseSettings(BaseSettings):
    url: str = "sqlite+aiosqlite:///./crm.db"
    echo: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_")


class Settings(BaseSettings):
    load_dotenv()
    srv: SrvSettings = SrvSettings()
    database: DatabaseSettings = DatabaseSettings()


settings = Settings()
