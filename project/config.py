from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Any

load_dotenv(override=True)


class Settings(BaseSettings):
    # Logging
    silent: bool = False
    log_path: str = '.logs'
    log_level: str = 'INFO'
    log_format: str = '%(levelname)s: %(asctime)s %(message)s'
    date_format: str = '%H:%M:%S %d.%m.%Y'

    # Postgres DB
    postgres_host: str = ''
    postgres_port: str = ''
    postgres_db_name: str = ''
    postgres_db_user: str = ''
    postgres_db_password: str = ''
    
    # DB Config
    @property
    def db_config(self) -> dict[str, Any]:
        return {
            'dbname': self.postgres_db_name,
            'user': self.postgres_db_user,
            'password': self.postgres_db_password,
            'host': self.postgres_host,
            'port': self.postgres_port
        }

    # API
    ml_api: str = ''
    back_api: str = ''

    # Encryption
    secret_key: str = ''
    encryption_algorithm: str = ''
    access_token_expire_seconds: str = ''

    # Path
    data_path: str = '__data__'


settings = Settings()
