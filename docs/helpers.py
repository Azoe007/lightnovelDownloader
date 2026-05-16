import re
import requests

from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ============================================
# REQUEST HTML
# ============================================

def get_soup(url, timeout=20):

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=timeout
    )

    r.raise_for_status()

    return BeautifulSoup(r.text, "lxml")


# ============================================
# REQUEST JSON
# ============================================

def get_json(url, timeout=20):

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=timeout
    )

    r.raise_for_status()

    return r.json()


# ============================================
# DOWNLOAD BINARY
# ============================================

def download_file(url, timeout=20):

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=timeout
    )

    r.raise_for_status()

    return r.content


# ============================================
# CLEAN FILENAME
# ============================================

def sanitize_filename(name):

    return re.sub(
        r'[\\/*?:"<>|]',
        "",
        name
    )


# ============================================
# CLEAN HTML
# ============================================

def clean_content(content):

    for tag in content([
        "script",
        "style",
        "iframe",
        "ins",
        "ads"
    ]):
        tag.decompose()

    return str(content)


# ============================================
# EPUB CSS
# ============================================

EPUB_CSS = """
body {
    font-family: Georgia, serif;
    font-size: 1.08em;
    line-height: 1.8;
    margin: 6%;
    text-align: justify;
    color: #111;
    background: #fdfdfd;
}

h1 {
    text-align: center;
    font-size: 1.9em;
    margin: 2em 0 1em;
}

p {
    margin: 0.9em 0;
    text-indent: 1.6em;
}
"""