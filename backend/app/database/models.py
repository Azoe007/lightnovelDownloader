from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, Enum as SQLEnum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database.db import Base


class DownloadStatus(str, enum.Enum):
    """Statut d'un téléchargement"""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class Novel(Base):
    """Modèle d'un novel"""
    __tablename__ = "novels"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    author = Column(String(300), nullable=True)
    description = Column(Text, nullable=True)
    cover_url = Column(String(500), nullable=True)
    cover_path = Column(String(500), nullable=True)
    source_url = Column(String(500), nullable=False)
    source_site = Column(String(100), nullable=False)
    
    total_chapters = Column(Integer, default=0)
    language = Column(String(10), default="fr")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    downloads = relationship("Download", back_populates="novel", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="novel", cascade="all, delete-orphan")


class Download(Base):
    """Modèle d'un téléchargement en cours ou terminé"""
    __tablename__ = "downloads"
    
    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"), nullable=False)
    
    status = Column(SQLEnum(DownloadStatus), default=DownloadStatus.PENDING)
    progress = Column(Float, default=0.0)
    current_chapter = Column(Integer, default=0)
    total_chapters = Column(Integer, default=0)
    
    current_chapter_title = Column(String(500), nullable=True)
    
    speed = Column(Float, default=0.0)
    eta = Column(Integer, default=0)
    
    output_path = Column(String(500), nullable=True)
    file_size = Column(Integer, default=0)
    
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    novel = relationship("Novel", back_populates="downloads")


class Favorite(Base):
    """Modèle des favoris"""
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"), nullable=False)
    
    tags = Column(JSON, default=list)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    novel = relationship("Novel", back_populates="favorites")


class History(Base):
    """Historique des téléchargements terminés"""
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"), nullable=False)
    
    chapters_downloaded = Column(Integer, default=0)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    
    downloaded_at = Column(DateTime, default=datetime.utcnow)