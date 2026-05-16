from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Application
    APP_NAME: str = "LNCrawler API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./ln crawler.db"
    
    # Storage
    DOWNLOAD_DIR: str = "./downloads"
    COVER_DIR: str = "./covers"
    
    # Scraping
    REQUEST_TIMEOUT: int = 30
    MAX_CONCURRENT_DOWNLOADS: int = 3
    CHAPTER_DELAY: float = 0.5  # Délai entre les chapitres (secondes)
    
    class Config:
        env_file = ".env"


settings = Settings()

# Créer les dossiers de stockage
os.makedirs(settings.DOWNLOAD_DIR, exist_ok=True)
os.makedirs(settings.COVER_DIR, exist_ok=True)