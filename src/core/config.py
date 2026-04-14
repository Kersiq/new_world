from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field, SecretStr
from pathlib import Path


class Web(BaseModel):
    host: str
    port: int


class Db(BaseModel):
    host: str
    port: int
    username: str
    password: SecretStr
    db_name: str


class Config(BaseSettings):
    web: Web = Field(default_factory=Web)
    db: Db = Field(default_factory=Db)

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_nested_delimiter="__"
    )

    def get_postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.db.username}:"
            f"{self.db.password.get_secret_value()}@"
            f"{self.db.host}:{self.db.port}/"
            f"{self.db.db_name}"
        )


def get_config():
    return  Config()
