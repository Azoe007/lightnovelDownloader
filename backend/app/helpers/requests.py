import re
import requests
from bs4 import BeautifulSoup
from typing import Any

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_soup(url: str, timeout: int = 20) -> BeautifulSoup:
    """Récupère le HTML d'une URL et retourne un objet BeautifulSoup"""
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml")


def get_json(url: str, timeout: int = 20) -> Any:
    """Récupère le JSON d'une URL"""
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.json()


def download_file(url: str, timeout: int = 20) -> bytes:
    """Télécharge un fichier binaire"""
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.content