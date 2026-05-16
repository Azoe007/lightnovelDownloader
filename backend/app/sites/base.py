from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseSite(ABC):
    """Classe de base pour tous les scrapers de sites"""
    
    BASE_URL: str = ""
    
    def __init__(self, novel_url: str):
        """Initialise le scraper avec l'URL du novel"""
        self.novel_url = novel_url
    
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Vérifie si ce scraper peut gérer l'URL donnée"""
        pass
    
    @abstractmethod
    def get_title(self) -> str:
        """Récupère le titre du novel"""
        pass
    
    @abstractmethod
    def fetch_cover(self) -> Optional[bytes]:
        """Télécharge la couverture du novel"""
        pass
    
    @abstractmethod
    def fetch_all_chapters(self) -> List[Dict[str, Any]]:
        """Récupère la liste de tous les chapitres"""
        pass
    
    @abstractmethod
    def fetch_chapter(self, url: str) -> Dict[str, str]:
        """Récupère le contenu d'un chapitre"""
        pass
    
    def get_author(self) -> Optional[str]:
        """Récupère l'auteur du novel (optionnel)"""
        return None
    
    def get_description(self) -> Optional[str]:
        """Récupère la description du novel (optionnel)"""
        return None