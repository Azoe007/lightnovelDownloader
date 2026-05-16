from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database.db import get_db
from app.database.models import Download, DownloadStatus, Novel
from app.schemas.download import DownloadCreate, DownloadResponse, DownloadProgress
from app.core.download_manager import download_manager
from app.sites.registry import registry
import uuid

router = APIRouter(prefix="/api/downloads", tags=["Downloads"])


@router.post("", response_model=DownloadResponse)
async def start_download(
    download_data: DownloadCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Démarre un nouveau téléchargement"""
    
    # Vérifie que le site est supporté
    try:
        registry.get_site(download_data.url)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Site non supporté"
        )
    
    # Crée le novel (sera mis à jour pendant le download)
    # Utilise un slug temporaire unique pour éviter les collisions sur la contrainte UNIQUE
    temp_slug = f"pending-{uuid.uuid4().hex[:8]}"
    novel = Novel(
        title="Pending...",
        slug=temp_slug,
        source_url=download_data.url,
        source_site="unknown"
    )
    db.add(novel)
    await db.flush()
    
    # Crée le download
    download = Download(
        status=DownloadStatus.PENDING,
        novel_id=novel.id
    )
    db.add(download)
    await db.commit()
    await db.refresh(download)
    
    # Démarre le téléchargement en background
    background_tasks.add_task(
        download_manager.start_download,
        download_data.url,
        download.id
    )
    
    return download


@router.get("", response_model=List[DownloadResponse])
async def get_downloads(
    status: DownloadStatus = None,
    db: AsyncSession = Depends(get_db)
):
    """Récupère la liste des téléchargements"""
    
    query = select(Download)
    
    if status:
        query = query.where(Download.status == status)
    
    result = await db.execute(query)
    downloads = result.scalars().all()
    
    return downloads


@router.get("/{download_id}", response_model=DownloadResponse)
async def get_download(
    download_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Récupère les détails d'un téléchargement"""
    
    result = await db.execute(
        select(Download).where(Download.id == download_id)
    )
    download = result.scalar_one_or_none()
    
    if not download:
        raise HTTPException(status_code=404, detail="Download introuvable")
    
    return download


@router.post("/{download_id}/pause")
async def pause_download(
    download_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Met en pause un téléchargement"""
    
    await download_manager.pause_download(download_id)
    return {"message": "Download paused"}


@router.post("/{download_id}/resume")
async def resume_download(
    download_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Reprend un téléchargement en pause"""
    
    await download_manager.resume_download(download_id)
    return {"message": "Download resumed"}


@router.delete("/{download_id}")
async def cancel_download(
    download_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Annule un téléchargement"""
    
    await download_manager.cancel_download(download_id)
    return {"message": "Download cancelled"}