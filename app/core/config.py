from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PORT: int = 8006
    JWT_SECRET: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "readme"
    DB_PASSWORD: str = "readme123"
    DB_NAME: str = "ms6_transactions"
    ADMIN_KEY: str = ""
    ALLOWED_ORIGINS: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
