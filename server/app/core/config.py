from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    blinker_db_path: str = 'server/data/blinker.db'
    blinker_media_dir: str = 'server/data/media'
    blinker_poll_seconds: int = 30
    blinker_ai_provider: str = 'none'
    blinker_ollama_url: str = 'http://localhost:11434'
    blinker_ollama_model: str = 'llama3.1'
    blinker_auto_download_clips: bool = True
    blinker_bind_host: str = '127.0.0.1'
    blinker_port: int = 8090
    blinker_use_mock: bool = False

    @property
    def db_url(self) -> str:
        path = Path(self.blinker_db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return f'sqlite:///{path}'


settings = Settings()
