import re
from bs4 import BeautifulSoup


def sanitize_filename(name: str) -> str:
    """Nettoie un nom de fichier des caractères interdits"""
    return re.sub(r'[\\/*?:"<>|]', "", name)


def clean_content(content: BeautifulSoup) -> str:
    """Nettoie le contenu HTML d'un chapitre"""
    # Supprime les éléments indésirables
    for tag in content([
        "script",
        "style",
        "iframe",
        "ins",
        "ads",
        ".ad",
        ".advertisement",
        ".related-posts",
        ".comments"
    ]):
        tag.decompose()
    
    return str(content)


def clean_html_tags(html: str) -> str:
    """Nettoie les balises HTML indésirables"""
    # Supprime les balises script et style
    cleaned = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'<style.*?</style>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    
    return cleaned