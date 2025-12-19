from pydantic_settings import BaseSettings
from datetime import timedelta
from urllib.parse import quote_plus


class Settings(BaseSettings):
    mysql_user: str
    mysql_password: str
    mysql_host: str
    mysql_port: int
    mysql_db: str

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    # KORPAY
    mid: str
    mkey: str
    sms_api_url: str
    manual_api_url: str

    #popbill
    LinkID: str
    SecretKey: str
    IsTest: str
    IPRestrictOnOff: str
    UseStaticIP: str
    UseLocalTimeYN: str

    class Config:
        env_file = ".env"

    @property
    def encoded_password(self) -> str:
        return quote_plus(self.mysql_password)

    @property
    def database_url(self) -> str:
        return (
            f"mysql+mysqldb://{self.mysql_user}:{self.encoded_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}?charset=utf8mb4"
        )

    @property
    def access_token_expires(self):
        return timedelta(minutes=self.access_token_expire_minutes)

    @property
    def refresh_token_expires(self):
        return timedelta(days=self.refresh_token_expire_days)


settings = Settings()
