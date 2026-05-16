import asyncio
import os
import time
from datetime import datetime
from typing import Optional, Callable, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database.models import Download, DownloadStatus, Novel
from app.database.db import async_session_maker
from app.sites.registry import registry
from app.core.epub_builder import EPUBBuilder
from app.core.exceptions import DownloadError, SiteNotSupported
from app.helpers.cleaner import sanitize_filename


class DownloadManager:
    """Gère les téléchargements en cours"""
    
    def __init__(self):
        self.active_downloads: Dict[int, asyncio.Task] = {}
        self._running = True
    
    async def start_download(
        self,
        url: str,
        download_id: int
    ) -> None:
        """Démarre un téléchargement"""
        
        try:
            # Trouve le scraper approprié
            site = registry.get_site(url)
            
            async with async_session_maker() as db:
                # Récupère le download
                result = await db.execute(
                    select(Download).where(Download.id == download_id)
                )
                download = result.scalar_one_or_none()
                
                if not download:
                    raise DownloadError("Download introuvable")
                
                # Récupère les infos du novel
                title = site.get_title()
                author = site.get_author()
                description = site.get_description()
                
                # Met à jour le novel
                novel = download.novel
                novel.title = title
                novel.author = author
                novel.description = description
                novel.source_url = url
                novel.source_site = site.__class__.__name__
                novel.slug = url.rstrip("/").split("/")[-1]
                
                await db.flush()
                
                # Met à jour le download
                download.status = DownloadStatus.DOWNLOADING
                download.started_at = datetime.utcnow()
                download.novel_id = novel.id
                
                await db.flush()
                
                # Récupère les chapitres
                chapters = site.fetch_all_chapters()
                download.total_chapters = len(chapters)
                novel.total_chapters = len(chapters)
                
                # Télécharge la couverture
                cover_data = site.fetch_cover()
                cover_path = None
                
                if cover_data:
                    cover_filename = f"{sanitize_filename(title)}_cover.jpg"
                    cover_path = os.path.join(settings.COVER_DIR, cover_filename)
                    with open(cover_path, "wb") as f:
                        f.write(cover_data)
                    novel.cover_path = cover_path
                
                await db.flush()
                
                # Construit l'EPUB
                builder = EPUBBuilder(site)
                
                def progress_callback(current: int, total: int, chapter_title: str):
                    """Callback pour mettre à jour la progression"""
                    # Schedule an async DB update from the worker thread
                    async def _update_progress():
                        async with async_session_maker() as _db:
                            res = await _db.execute(
                                select(Download).where(Download.id == download_id)
                            )
                            _download = res.scalar_one_or_none()
                            if not _download:
                                return

                            _download.current_chapter = current
                            _download.current_chapter_title = chapter_title
                            # avoid division by zero
                            if total and total > 0:
                                _download.progress = (current / total) * 100
                            else:
                                _download.progress = 0.0

                            # Calcule la vitesse
                            if _download.started_at:
                                elapsed = (datetime.utcnow() - _download.started_at).total_seconds()
                                if elapsed > 0:
                                    _download.speed = current / elapsed

                            # Calcule l'ETA
                            remaining = total - current
                            if _download.speed and _download.speed > 0:
                                _download.eta = int(remaining / _download.speed)

                            await _db.commit()

                    try:
                        loop = asyncio.get_running_loop()
                        # If called from a thread (builder runs in thread), schedule safely
                        asyncio.run_coroutine_threadsafe(_update_progress(), loop)
                    except RuntimeError:
                        # Fallback: if no running loop, run coroutine in a new task
                        asyncio.create_task(_update_progress())
                
                # Construit l'EPUB de manière synchrone (dans un thread)
                output_path = await asyncio.to_thread(
                    builder.build,
                    title=title,
                    chapters=chapters,
                    author=author,
                    cover_data=cover_data,
                    progress_callback=progress_callback
                )
                
                # Marque comme terminé
                download.status = DownloadStatus.COMPLETED
                download.completed_at = datetime.utcnow()
                download.output_path = output_path
                download.file_size = os.path.getsize(output_path)
                download.progress = 100.0
                
                await db.commit()
                
        except Exception as e:
            # Gère les erreurs
            async with async_session_maker() as db:
                result = await db.execute(
                    select(Download).where(Download.id == download_id)
                )
                download = result.scalar_one_or_none()
                
                if download:
                    download.status = DownloadStatus.FAILED
                    download.error_message = str(e)
                    download.retry_count += 1
                    await db.commit()
            
            raise
    
    async def pause_download(self, download_id: int) -> None:
        """Met en pause un téléchargement"""
        async with async_session_maker() as db:
            result = await db.execute(
                select(Download).where(Download.id == download_id)
            )
            download = result.scalar_one_or_none()
            
            if download and download.status == DownloadStatus.DOWNLOADING:
                download.status = DownloadStatus.PAUSED
                await db.commit()
    
    async def resume_download(self, download_id: int) -> None:
        """Reprend un téléchargement en pause"""
        async with async_session_maker() as db:
            result = await db.execute(
                select(Download).where(Download.id == download_id)
            )
            download = result.scalar_one_or_none()
            
            if download and download.status == DownloadStatus.PAUSED:
                download.status = DownloadStatus.DOWNLOADING
                await db.commit()
    
    async def cancel_download(self, download_id: int) -> None:
        """Annule un téléchargement"""
        async with async_session_maker() as db:
            result = await db.execute(
                select(Download).where(Download.id == download_id)
            )
            download = result.scalar_one_or_none()
            
            if download:
                download.status = DownloadStatus.CANCELLED
                await db.commit()
            
            # Supprime la tâche si elle existe
            if download_id in self.active_downloads:
                self.active_downloads[download_id].cancel()
                del self.active_downloads[download_id]


# Instance globale
download_manager = DownloadManager()