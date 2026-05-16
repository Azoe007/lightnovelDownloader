import time

from sites.base import BaseSite

from utils.helpers import (
    get_json,
    get_soup,
    download_file,
    clean_content
)


class NovelFrance(BaseSite):

    BASE_URL = "https://novelfrance.fr"

    TAKE = 50

    def __init__(self, novel_url):

        super().__init__(novel_url)

        self.slug = (
            novel_url
            .rstrip("/")
            .split("/")[-1]
        )

        self.api_url = (
            f"{self.BASE_URL}"
            f"/api/chapters/{self.slug}"
        )

        self.info_url = (
            f"{self.BASE_URL}"
            f"/api/novels/{self.slug}"
        )

    # ============================================
    # TITLE
    # ============================================

    def get_title(self):

        data = get_json(self.info_url)

        return data.get(
            "title",
            self.slug
        )

    # ============================================
    # COVER
    # ============================================

    def fetch_cover(self):

        try:

            data = get_json(self.info_url)

            cover = (
                data.get("cover")
                or data.get("coverUrl")
            )

            if not cover:
                return None

            if cover.startswith("/"):
                cover = (
                    self.BASE_URL + cover
                )

            return download_file(cover)

        except:
            return None

    # ============================================
    # FETCH ALL CHAPTERS
    # ============================================

    def fetch_all_chapters(self):

        chapters = []

        seen = set()

        skip = 0
        has_more = True

        while has_more:

            print(f"→ skip={skip}")

            url = (
                f"{self.api_url}"
                f"?skip={skip}"
                f"&take={self.TAKE}"
                f"&order=desc"
            )

            data = get_json(url)

            batch = data.get(
                "chapters",
                []
            )

            has_more = data.get(
                "hasMore",
                False
            )

            if not batch:
                break

            for item in batch:

                title = item.get("title")

                slug = item.get("slug")

                number = item.get(
                    "chapterNumber"
                )

                if not slug:
                    continue

                chapter_url = (
                    f"{self.BASE_URL}"
                    f"/novel/{self.slug}/{slug}"
                )

                if chapter_url in seen:
                    continue

                seen.add(chapter_url)

                chapters.append({
                    "title": title,
                    "chapterNumber": number,
                    "url": chapter_url
                })

            skip += self.TAKE

            time.sleep(0.2)

        chapters.sort(
            key=lambda x: x["chapterNumber"]
        )

        return chapters

    # ============================================
    # FETCH CHAPTER
    # ============================================

    def fetch_chapter(self, url):

        soup = get_soup(url)

        title = soup.find("h1")

        title = (
            title.get_text(strip=True)
            if title
            else "Chapitre"
        )

        content = soup.select_one(
            "div.reading-content, "
            "div.entry-content, "
            "div.chapter-content"
        )

        if not content:
            raise Exception(
                "Contenu introuvable"
            )

        return {
            "title": title,
            "content": clean_content(content)
        }