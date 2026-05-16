class LNCrawlerException(Exception):
    """Exception de base pour LNCrawler"""
    pass


class SiteNotSupported(LNCrawlerException):
    """Le site n'est pas supporté"""
    pass


class ChapterNotFound(LNCrawlerException):
    """Chapitre introuvable"""
    pass


class DownloadError(LNCrawlerException):
    """Erreur lors du téléchargement"""
    pass


class EPUBBuildError(LNCrawlerException):
    """Erreur lors de la création de l'EPUB"""
    pass


class DatabaseError(LNCrawlerException):
    """Erreur de base de données"""
    pass