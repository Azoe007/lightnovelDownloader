import re
import time
import logging
import requests
from bs4 import BeautifulSoup
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

# Use a session to persist headers/cookies across requests
_session = requests.Session()
_session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
})

# If a proxy is configured via env, apply it (format: http://host:port)
import os
_proxy = os.environ.get('SCRAPER_PROXY')
if _proxy:
    logger.info('Using SCRAPER_PROXY=%s', _proxy)
    _session.proxies.update({
        'http': _proxy,
        'https': _proxy,
    })


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
    final_headers = _session.headers.copy()
    if headers:
        final_headers.update(headers)

    attempt = 0
    while attempt < max_retries:
        try:
            logger.debug("HTTP %s %s (attempt %d)", method, url, attempt + 1)
            resp = _session.request(method, url, headers=final_headers, timeout=timeout)

            # If 403 and host looks like novelfrance, try adding Referer and X-Requested-With
            if resp.status_code == 403 and 'novelfrance' in url.lower():
                logger.info("Received 403 from %s, retrying with Referer/X-Requested-With", url)
                # add headers and retry once
                final_headers.update({
                    'Referer': 'https://novelfrance.fr',
                    'X-Requested-With': 'XMLHttpRequest',
                })
                resp = _session.request(method, url, headers=final_headers, timeout=timeout)

            # Log non-200 for troubleshooting and include small body snippet
            if resp.status_code >= 400:
                body_snippet = ''
                try:
                    body = resp.text
                    body_snippet = body[:400].replace('\n', ' ')
                except Exception:
                    body_snippet = '<no body>'
                logger.warning("HTTP %s returned %d for %s - body: %s", method, resp.status_code, url, body_snippet)

            resp.raise_for_status()
            return resp
        except requests.HTTPError as he:
            attempt += 1
            logger.debug("HTTPError on attempt %d for %s: %s", attempt, url, he)
            if attempt >= max_retries:
                logger.error("Max retries reached for %s", url)
                raise
            time.sleep(0.5 * attempt)
        except requests.RequestException as rexc:
            attempt += 1
            logger.debug("RequestException on attempt %d for %s: %s", attempt, url, rexc)
            if attempt >= max_retries:
                logger.error("Max retries reached for %s", url)
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