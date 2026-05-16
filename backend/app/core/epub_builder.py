import os
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

from ebooklib import epub
from app.config import settings
from app.helpers.epub import EPUB_CSS
from app.helpers.cleaner import sanitize_filename
from app.sites.base import BaseSite


class EPUBBuilder:
    """Constructeur de fichiers EPUB"""
    
    def __init__(self, site: BaseSite):
        self.site = site
        self.book = epub.EpubBook()
        self.css = None
    
    def _setup_book(self, title: str, author: Optional[str] = None):
        """Configure le livre EPUB"""
        self.book.set_title(title)
        self.book.set_language("fr")
        self.book.add_author(author or "LNCrawler")
        
        # Ajoute le CSS
        self.css = epub.EpubItem(
            uid="style",
            file_name="style/style.css",
            media_type="text/css",
            content=EPUB_CSS
        )
        self.book.add_item(self.css)
    
    def _add_cover(self, cover_data: Optional[bytes]):
        """Ajoute la couverture"""
        if cover_data:
            self.book.set_cover("cover.jpg", cover_data)
    
    def _add_chapter(self, index: int, chapter_data: Dict[str, str]) -> epub.EpubHtml:
        """Ajoute un chapitre au livre"""
        chapter = epub.EpubHtml(
            title=f"Chapitre {chapter_data.get('chapterNumber', index + 1)}",
            file_name=f"chap_{index}.xhtml"
        )
        
        chapter.content = f"""
        <h1>Chapitre {chapter_data.get('chapterNumber', index + 1)}: {chapter_data['title']}</h1>
        {chapter_data['content']}
        """
        
        chapter.add_item(self.css)
        self.book.add_item(chapter)
        
        return chapter
    
    def build(
        self,
        title: str,
        chapters: List[Dict[str, Any]],
        author: Optional[str] = None,
        cover_data: Optional[bytes] = None,
        output_dir: Optional[str] = None,
        progress_callback=None
    ) -> str:
        """Construit l'EPUB complet"""
        
        # Setup
        self._setup_book(title, author)
        self._add_cover(cover_data)
        
        # Ajoute les chapitres
        epub_chapters = []
        total = len(chapters)
        
        for i, chapter_info in enumerate(chapters):
            try:
                # Récupère le contenu du chapitre
                chapter_data = self.site.fetch_chapter(chapter_info["url"])
                
                # Ajoute au livre
                chapter = self._add_chapter(i, chapter_data)
                epub_chapters.append(chapter)
                
                # Callback de progression
                if progress_callback:
                    progress_callback(i + 1, total, chapter_info.get("title", ""))
                
                # Délai pour éviter de spammer
                time.sleep(settings.CHAPTER_DELAY)
                
            except Exception as e:
                print(f"Erreur chapitre {i+1}: {e}")
                if progress_callback:
                    progress_callback(i + 1, total, f"Erreur: {chapter_info.get('title', '')}")
        
        # Structure EPUB
        self.book.toc = tuple(epub_chapters)
        self.book.spine = ["nav"] + epub_chapters
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        
        # Génère le nom de fichier
        filename = sanitize_filename(title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        epub_filename = f"{filename}_{timestamp}.epub"
        
        # Détermine le dossier de sortie
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = settings.DOWNLOAD_DIR
        
        output_path = os.path.join(output_dir, epub_filename)
        
        # Écrit le fichier
        epub.write_epub(output_path, self.book, {})
        
        return output_path