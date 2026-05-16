from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from app.database.db import get_db
from app.database.models import History, Novel
from app.schemas.novel import NovelResponse

router = APIRouter(prefix="/api/history", tags=["History"])


@router.get("", response_model=List[NovelResponse])
async def get_history(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Récupère l'historique des téléchargements"""
    
    result = await db.execute(
        select(History).order_by(desc(History.downloaded_at)).offset(skip).limit(limit)
    )
    history_items = result.scalars().all()
    
    # Récupère les novels associés
    novel_ids = [h.novel_id for h in history_items]
    novels_result = await db.execute(
        select(Novel).where(Novel.id.in_(novel_ids))
    )
    novels = novels_result.scalars().all()
    
    return novels