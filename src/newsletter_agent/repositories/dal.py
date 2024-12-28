import os
import sqlite3

DB_FILE = "articles.db"

ARTICLE_TABLES_DDL = """
CREATE TABLE IF NOT EXISTS articles (
    url TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title TEXT,
    summary TEXT
);
""".strip()

INDEX_DDL = """
CREATE INDEX idx_created_at ON articles(created_at);
""".strip()


class DB:
    def __init__(self):
        self._create_database()
        self.conn = sqlite3.connect(DB_FILE)

    @classmethod
    def _create_database(cls) -> None:
        if os.path.exists(DB_FILE):
            return
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute(ARTICLE_TABLES_DDL)
            cursor.execute(INDEX_DDL)
            connection.commit()

    def query(self, sql: str, *args) -> list[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.row_factory = sqlite3.Row
        try:
            cur.execute(sql, args)
            return cur.fetchall()
        finally:
            cur.close()

    def execute(self, sql: str, args: tuple | list[tuple]) -> None:
        cur = self.conn.cursor()
        try:
            if isinstance(args, tuple):
                cur.execute(sql, args)
            else:
                cur.executemany(sql, args)
            self.conn.commit()
        finally:
            cur.close()


db = DB()
