from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.database.models import DownloadStatus


class DownloadCreate(BaseModel):
    """Schéma pour démarrer un téléchargement"""
    url: str


class DownloadResponse(BaseModel):
    """Schéma de réponse pour un téléchargement"""
    id: int
    novel_id: int
    status: DownloadStatus
    progress: float
    current_chapter: int
    total_chapters: int
    current_chapter_title: Optional[str] = None
    speed: float
    eta: int
    output_path: Optional[str] = None
    file_size: int
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DownloadProgress(BaseModel):
    """Schéma pour mettre à jour la progression"""
    status: Optional[DownloadStatus] = None
    progress: Optional[float] = None
    current_chapter: Optional[int] = None
    current_chapter_title: Optional[str] = None
    speed: Optional[float] = None
    eta: Optional[int] = None


class DownloadComplete(BaseModel):
    """Schéma pour marquer un téléchargement comme terminé"""
    output_path: str
    file_size: int
    chapters_downloaded: int