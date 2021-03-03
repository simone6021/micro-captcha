from pydantic import BaseSettings, RedisDsn


class Settings(BaseSettings):
    redis_dsn: RedisDsn = 'redis://redis:6379/1'
    captcha_id_ttl: int = 360
