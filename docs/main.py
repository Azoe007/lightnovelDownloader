import os
import time

from ebooklib import epub
from tqdm import tqdm

from sites.novelfrance import NovelFrance

from utils.helpers import (
    EPUB_CSS,
    sanitize_filename
)


OUTPUT_DIR = "output"


# ============================================
# SITE DETECTION
# ============================================

def get_site(url):

    if "novelfrance.fr" in url:
        return NovelFrance(url)

    raise Exception(
        "❌ Site non supporté"
    )


# ============================================
# EPUB BUILDER
# ============================================

def build_epub(site):

    title = site.get_title()

    print(f"\n📚 Novel : {title}")

    chapters = site.fetch_all_chapters()

    print(
        f"📖 Total chapitres : "
        f"{len(chapters)}"
    )

    # ============================================
    # BOOK
    # ============================================

    book = epub.EpubBook()

    book.set_title(title)

    book.set_language("fr")

    book.add_author("NovelFrance")

    # ============================================
    # COVER
    # ============================================

    cover = site.fetch_cover()

    if cover:

        book.set_cover(
            "cover.jpg",
            cover
        )

        print("🖼️ Cover ajoutée")

    # ============================================
    # CSS
    # ============================================

    css = epub.EpubItem(
        uid="style",
        file_name="style/style.css",
        media_type="text/css",
        content=EPUB_CSS
    )

    book.add_item(css)

    # ============================================
    # CHAPTERS
    # ============================================

    epub_chapters = []

    print("\n📦 Génération EPUB...\n")

    for i, ch in enumerate(
        tqdm(chapters)
    ):

        try:

            data = site.fetch_chapter(
                ch["url"]
            )

            chapter = epub.EpubHtml(
                title=(
                    f"Chapitre "
                    f"{ch['chapterNumber']}"
                ),
                file_name=f"chap_{i}.xhtml"
            )

            chapter.content = f"""
            <h1>
            Chapitre {ch['chapterNumber']}
            : {data['title']}
            </h1>

            {data['content']}
            """

            chapter.add_item(css)

            book.add_item(chapter)

            epub_chapters.append(
                chapter
            )

            time.sleep(0.2)

        except Exception as e:

            print(
                f"\n❌ Erreur : "
                f"{ch['url']}"
            )

            print(e)

    # ============================================
    # EPUB STRUCTURE
    # ============================================

    book.toc = tuple(epub_chapters)

    book.spine = (
        ["nav"] + epub_chapters
    )

    book.add_item(epub.EpubNcx())

    book.add_item(epub.EpubNav())

    # ============================================
    # EXPORT
    # ============================================

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    filename = sanitize_filename(
        title
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{filename}.epub"
    )

    epub.write_epub(
        output_path,
        book
    )

    print(
        f"\n✅ EPUB créé : "
        f"{output_path}"
    )


# ============================================
# MAIN
# ============================================

def main():

    url = input(
        "📘 URL DU NOVEL :\n> "
    ).strip()

    site = get_site(url)

    build_epub(site)


if __name__ == "__main__":
    main()