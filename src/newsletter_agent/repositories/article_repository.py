from newsletter_agent.models.article import Article

from .dal import db


class ArticleRepository:
    @classmethod
    def find_by_url(cls, url: str) -> Article | None:
        rows = db.query("SELECT * FROM articles WHERE url = ?", url)
        if not rows:
            return None
        row = dict(rows[0])
        return Article(**row)

    @classmethod
    def insert(cls, *article: Article) -> None:
        db.execute(
            "INSERT INTO articles (url, title, summary) VALUES (?, ?, ?)",
            [(a.url, a.title, a.summary) for a in article],
        )
