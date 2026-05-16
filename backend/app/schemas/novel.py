from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class NovelBase(BaseModel):
    """Schéma de base pour un novel"""
    title: str
    source_url: str
    source_site: str
    author: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    language: str = "fr"


class NovelCreate(NovelBase):
    """Schéma pour créer un novel"""
    pass


class NovelUpdate(BaseModel):
    """Schéma pour mettre à jour un novel"""
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    language: Optional[str] = None


class NovelResponse(NovelBase):
    """Schéma de réponse pour un novel"""
    id: int
    slug: str
    cover_path: Optional[str] = None
    total_chapters: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChapterInfo(BaseModel):
    """Informations sur un chapitre"""
    title: str
    chapterNumber: Optional[int] = None
    url: str


class NovelWithChapters(NovelResponse):
    """Novel avec liste des chapitres"""
    chapters: List[ChapterInfo] = []