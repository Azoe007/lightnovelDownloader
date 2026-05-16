import time
from typing import List, Dict, Any, Optional

from app.sites.base import BaseSite
from app.helpers.requests import get_json, get_soup, download_file
from app.helpers.cleaner import clean_content


class NovelFrance(BaseSite):
    """Scraper pour NovelFrance.fr"""
    
    BASE_URL = "https://novelfrance.fr"
    TAKE = 50
    
    def __init__(self, novel_url: str):
        super().__init__(novel_url)
        
        # Extrait le slug de l'URL
        self.slug = novel_url.rstrip("/").split("/")[-1]
        
        # URLs API
        self.api_url = f"{self.BASE_URL}/api/chapters/{self.slug}"
        self.info_url = f"{self.BASE_URL}/api/novels/{self.slug}"
    
    def can_handle(self, url: str) -> bool:
        """Vérifie si l'URL appartient à NovelFrance"""
        return "novelfrance.fr" in url
    
    def get_title(self) -> str:
        """Récupère le titre du novel"""
        try:
            data = get_json(self.info_url)
            return data.get("title", self.slug)
        except Exception:
            # fallback: parse the HTML page
            soup = get_soup(f"{self.BASE_URL}/novel/{self.slug}")
            h1 = soup.find("h1")
            if h1:
                return h1.get_text(strip=True)
            return self.slug
    
    def get_author(self) -> Optional[str]:
        """Récupère l'auteur du novel"""
        try:
            data = get_json(self.info_url)
            return data.get("author")
        except Exception:
            soup = get_soup(f"{self.BASE_URL}/novel/{self.slug}")
            # try common selectors
            author_elem = soup.select_one('.author, .post-author, .byline')
            if author_elem:
                return author_elem.get_text(strip=True)
            return None
    
    def get_description(self) -> Optional[str]:
        """Récupère la description du novel"""
        try:
            data = get_json(self.info_url)
            return data.get("description") or data.get("synopsis")
        except Exception:
            soup = get_soup(f"{self.BASE_URL}/novel/{self.slug}")
            desc = soup.select_one('.summary, .description, .entry-summary')
            if desc:
                return desc.get_text(strip=True)
            # meta description
            meta = soup.find('meta', {'name': 'description'})
            if meta and meta.get('content'):
                return meta.get('content')
            return None
    
    def fetch_cover(self) -> Optional[bytes]:
        """Télécharge la couverture du novel"""
        try:
            data = get_json(self.info_url)
            cover = data.get("cover") or data.get("coverUrl")
            
            if not cover:
                return None
            
            # Corrige l'URL si relative
            if cover.startswith("/"):
                cover = self.BASE_URL + cover
            
            return download_file(cover)
        
        except Exception:
            return None
    
    def fetch_all_chapters(self) -> List[Dict[str, Any]]:
        """Récupère la liste de tous les chapitres"""
        chapters = []
        seen = set()

        # Premièrement, essaye l'API JSON (rapide)
        try:
            skip = 0
            has_more = True

            while has_more:
                url = f"{self.api_url}?skip={skip}&take={self.TAKE}&order=desc"
                data = get_json(url)

                batch = data.get("chapters", [])
                has_more = data.get("hasMore", False)

                if not batch:
                    break

                for item in batch:
                    title = item.get("title")
                    slug = item.get("slug")
                    number = item.get("chapterNumber")

                    if not slug:
                        continue

                    chapter_url = f"{self.BASE_URL}/novel/{self.slug}/{slug}"

                    if chapter_url in seen:
                        continue

                    seen.add(chapter_url)

                    chapters.append({
                        "title": title,
                        "chapterNumber": number,
                        "url": chapter_url
                    })

                skip += self.TAKE
                time.sleep(0.2)  # Évite de spammer l'API

            # Trie les chapitres par numéro
            chapters.sort(key=lambda x: x["chapterNumber"] if x["chapterNumber"] else 0)
            if chapters:
                return chapters

        except Exception:
            # Si l'API échoue (403 par ex.), on tombe en fallback HTML
            pass

        # Fallback: parse la page HTML principale et extrait les liens de chapitres
        try:
            page_url = f"{self.BASE_URL}/novel/{self.slug}"
            soup = get_soup(page_url)
            # Recherche tous les liens qui ressemblent à des chapitres
            anchors = soup.find_all('a', href=True)
            for a in anchors:
                href = a['href']
                # normalise
                if href.startswith('/'):
                    href_full = self.BASE_URL + href
                elif href.startswith(self.BASE_URL):
                    href_full = href
                else:
                    continue

                # correspond aux chapitres: /novel/{slug}/{chapter-slug}
                pattern = f"/novel/{self.slug}/"
                if pattern in href_full:
                    if href_full in seen:
                        continue
                    seen.add(href_full)

                    title_text = a.get_text(strip=True) or None
                    # try to extract chapter number from text or href
                    number = None
                    m = re.search(r"(\d+)(?!.*\d)", a.get_text() or '')
                    if m:
                        try:
                            number = int(m.group(1))
                        except Exception:
                            number = None

                    chapters.append({
                        "title": title_text,
                        "chapterNumber": number,
                        "url": href_full
                    })

            # Try to sort by chapterNumber when available
            chapters.sort(key=lambda x: x["chapterNumber"] if x["chapterNumber"] else 0)
            return chapters

        except Exception:
            # dernier recours: retourne liste vide
            return []
    
    def fetch_chapter(self, url: str) -> Dict[str, str]:
        """Récupère le contenu d'un chapitre"""
        soup = get_soup(url)
        
        # Récupère le titre
        title_elem = soup.find("h1")
        title = title_elem.get_text(strip=True) if title_elem else "Chapitre"
        
        # Récupère le contenu
        content = soup.select_one(
            "div.reading-content, "
            "div.entry-content, "
            "div.chapter-content"
        )
        
        if not content:
            raise Exception("Contenu introuvable")
        
        return {
            "title": title,
            "content": clean_content(content)
        }