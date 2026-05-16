from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database.db import get_db
from app.database.models import Novel, Download, DownloadStatus
from app.schemas.novel import NovelResponse

router = APIRouter(prefix="/api/library", tags=["Library"])


@router.get("", response_model=List[NovelResponse])
async def get_library(
    skip: int = 0,
    limit: int = 50,
    search: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Récupère la bibliothèque locale (novels téléchargés)"""
    
    query = select(Novel).join(Download).where(
        Download.status == DownloadStatus.COMPLETED
    )
    
    if search:
        query = query.where(Novel.title.ilike(f"%{search}%"))
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    novels = result.scalars().all()
    
    return novels


@router.get("/{novel_id}", response_model=NovelResponse)
async def get_novel(
    novel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Récupère les détails d'un novel"""
    
    result = await db.execute(
        select(Novel).where(Novel.id == novel_id)
    )
    novel = result.scalar_one_or_none()
    
    if not novel:
        raise HTTPException(status_code=404, detail="Novel introuvable")
    
    return novel


@router.delete("/{novel_id}")
async def delete_novel(
    novel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Supprime un novel de la bibliothèque"""
    
    result = await db.execute(
        select(Novel).where(Novel.id == novel_id)
    )
    novel = result.scalar_one_or_none()
    
    if not novel:
        raise HTTPException(status_code=404, detail="Novel introuvable")
    
    await db.delete(novel)
    await db.commit()
    
    return {"message": "Novel supprimé"}