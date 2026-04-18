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

    pool_max_size: int = 10


    def get_postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.username}:"
            f"{self.password.get_secret_value()}@"
            f"{self.host}:{self.port}/"
            f"{self.db_name}"
        )


class Config(BaseSettings):
    web: Web = Field(default_factory=Web)
    db: Db = Field(default_factory=Db)

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_nested_delimiter="__"
    )


def get_config():
    return  Config()

config = get_config()

print(config.__dict__)
