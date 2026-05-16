from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database.db import init_db
from app.api.routes import download, library, favorites, history
from app.sites.registry import registry
from app.sites.novelfrance import NovelFrance

# Enregistre les scrapers
registry.register(NovelFrance)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialisation de l'application"""
    # Crée la base de données
    await init_db()
    yield
    # Nettoyage à l'arrêt (si nécessaire)


# Crée l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API pour LNCrawler - Téléchargement de webnovels",
    lifespan=lifespan
)

# Configure CORS (pour permettre à Flutter de se connecter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistre les routes
app.include_router(download.router)
app.include_router(library.router)
app.include_router(favorites.router)
app.include_router(history.router)


@app.get("/")
async def root():
    """Endpoint de santé"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Vérifie que l'API est opérationnelle"""
    return {"status": "healthy"}