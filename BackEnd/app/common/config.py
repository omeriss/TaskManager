from functools import cached_property
from pathlib import Path
from pydantic import computed_field, PostgresDsn
from pydantic_settings import SettingsConfigDict, BaseSettings

PROJECT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # PROJECT NAME, VERSION AND DESCRIPTION
    PROJECT_NAME: str = "Task Manager"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for managing tasks"

    # CORS and HOSTS
    BACKEND_CORS_ORIGINS: list[str] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    # POSTGRESQL DEFAULT DATABASE
    DEFAULT_DATABASE_HOSTNAME: str
    DEFAULT_DATABASE_USER: str
    DEFAULT_DATABASE_PASSWORD: str
    DEFAULT_DATABASE_PORT: int
    DEFAULT_DATABASE_DB: str

    @computed_field
    @cached_property
    def DEFAULT_SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                username=self.DEFAULT_DATABASE_USER,
                password=self.DEFAULT_DATABASE_PASSWORD,
                host=self.DEFAULT_DATABASE_HOSTNAME,
                port=self.DEFAULT_DATABASE_PORT,
                path=self.DEFAULT_DATABASE_DB,
            )
        )

    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env", case_sensitive=True
    )


settings: Settings = Settings()  # type: ignore


