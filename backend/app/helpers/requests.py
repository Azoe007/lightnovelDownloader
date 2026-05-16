import re
import time
import requests
from bs4 import BeautifulSoup
from typing import Any, Dict, Optional

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}


def _request_with_retry(
    method: str,
    url: str,
    timeout: int = 20,
    headers: Optional[Dict[str, str]] = None,
    max_retries: int = 3,
) -> requests.Response:
    """Internal helper: perform a requests call with retries and a 403 fallback.

    On 403 we retry once with a Referer and X-Requested-With headers which
    some sites require for API endpoints.
    """
    final_headers = BASE_HEADERS.copy()
    if headers:
        final_headers.update(headers)

    attempt = 0
    while attempt < max_retries:
        try:
            resp = requests.request(method, url, headers=final_headers, timeout=timeout)
            # If 403 and host looks like novelfrance, try adding Referer and X-Requested-With
            if resp.status_code == 403 and 'novelfrance' in url.lower():
                # add headers and retry once
                final_headers.update({
                    'Referer': 'https://novelfrance.fr',
                    'X-Requested-With': 'XMLHttpRequest',
                })
                resp = requests.request(method, url, headers=final_headers, timeout=timeout)

            resp.raise_for_status()
            return resp
        except requests.HTTPError:
            # for HTTP errors, if last attempt re-raise
            attempt += 1
            if attempt >= max_retries:
                raise
            time.sleep(0.5 * attempt)
        except requests.RequestException:
            attempt += 1
            if attempt >= max_retries:
                raise
            time.sleep(0.5 * attempt)


def get_soup(url: str, timeout: int = 20, headers: Optional[Dict[str, str]] = None) -> BeautifulSoup:
    """Récupère le HTML d'une URL et retourne un objet BeautifulSoup"""
    r = _request_with_retry('GET', url, timeout=timeout, headers=headers)
    return BeautifulSoup(r.text, "lxml")


def get_json(url: str, timeout: int = 20, headers: Optional[Dict[str, str]] = None) -> Any:
    """Récupère le JSON d'une URL en gérant quelques protections simples."""
    r = _request_with_retry('GET', url, timeout=timeout, headers=headers)
    return r.json()


def download_file(url: str, timeout: int = 20, headers: Optional[Dict[str, str]] = None) -> bytes:
    """Télécharge un fichier binaire"""
    r = _request_with_retry('GET', url, timeout=timeout, headers=headers)
    return r.content