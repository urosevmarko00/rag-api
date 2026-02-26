from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    api_version: str
    debug: bool = False

    model_config = {
        "env_file": ".env"
    }


settings = Settings()
