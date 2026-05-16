from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database.db import get_db
from app.database.models import Favorite, Novel
from app.schemas.novel import NovelResponse

router = APIRouter(prefix="/api/favorites", tags=["Favorites"])


@router.get("", response_model=List[NovelResponse])
async def get_favorites(
    db: AsyncSession = Depends(get_db)
):
    """Récupère la liste des favoris"""
    
    result = await db.execute(select(Favorite))
    favorites = result.scalars().all()
    
    # Récupère les novels associés
    novel_ids = [fav.novel_id for fav in favorites]
    novels_result = await db.execute(
        select(Novel).where(Novel.id.in_(novel_ids))
    )
    novels = novels_result.scalars().all()
    
    return novels


@router.post("/{novel_id}")
async def add_favorite(
    novel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Ajoute un novel aux favoris"""
    
    # Vérifie que le novel existe
    result = await db.execute(
        select(Novel).where(Novel.id == novel_id)
    )
    novel = result.scalar_one_or_none()
    
    if not novel:
        raise HTTPException(status_code=404, detail="Novel introuvable")
    
    # Vérifie si déjà en favori
    existing = await db.execute(
        select(Favorite).where(Favorite.novel_id == novel_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Déjà en favori")
    
    # Ajoute le favori
    favorite = Favorite(novel_id=novel_id)
    db.add(favorite)
    await db.commit()
    
    return {"message": "Ajouté aux favoris"}


@router.delete("/{novel_id}")
async def remove_favorite(
    novel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Supprime un novel des favoris"""
    
    result = await db.execute(
        select(Favorite).where(Favorite.novel_id == novel_id)
    )
    favorite = result.scalar_one_or_none()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favori introuvable")
    
    await db.delete(favorite)
    await db.commit()
    
    return {"message": "Supprimé des favoris"}