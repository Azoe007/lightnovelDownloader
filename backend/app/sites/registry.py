from typing import Type, List
from app.sites.base import BaseSite


class SiteRegistry:
    """Registry pour gérer les différents scrapers de sites"""
    
    def __init__(self):
        self._sites: List[Type[BaseSite]] = []
    
    def register(self, site_class: Type[BaseSite]):
        """Enregistre un nouveau scraper"""
        self._sites.append(site_class)
    
    def get_site(self, url: str) -> BaseSite:
        """Retourne le scraper approprié pour une URL donnée"""
        for site_class in self._sites:
            # Crée une instance temporaire pour tester
            instance = site_class(url)
            if instance.can_handle(url):
                return instance
        
        raise ValueError(f"Aucun scraper trouvé pour l'URL: {url}")
    
    def get_supported_sites(self) -> List[str]:
        """Retourne la liste des sites supportés"""
        return [site_class.__name__ for site_class in self._sites]


# Registry globale
registry = SiteRegistry()