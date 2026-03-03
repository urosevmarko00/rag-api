from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    api_version: str
    debug: bool = False
    llm_provider: str = "local"  # ili openai

    model_config = {
        "env_file": ".env"
    }


settings = Settings()
