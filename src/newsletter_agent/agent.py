import json

from newsletter_agent.config import config
from newsletter_agent.logger import logger
from newsletter_agent.models.article import Article
from newsletter_agent.relevant_article_agent import (
    RelevantArticle,
    RelevantArticleAgent,
)
from newsletter_agent.repositories.article_repository import ArticleRepository
from newsletter_agent.scrape import scrape_and_extract_text
from newsletter_agent.summary_agent import SummaryAgent


class DailyUpdateAgent:
    def __init__(self):
        self.summary_agent = SummaryAgent()
        self.interesting_article_agent = RelevantArticleAgent()

    async def run(self) -> str:
        markdown = ["# Daily Update"]
        for source_name, url in config.sources.items():
            all_articles = await self._handle_source(source_name, url)
            articles = [a for a in all_articles if a.summary]
            if any(articles):
                markdown.append(f"## {source_name}")

            for i, article in enumerate(articles, 1):
                markdown.append(f"### {i}. [{article.title}]({article.url})")
                markdown.append(str(article.summary))
                markdown.append("")
                markdown.append("---")
            logger.info("---------------------")
            ArticleRepository.insert(*all_articles)
        return "\n".join(markdown)

    async def _handle_source(self, source_name: str, url: str) -> list[Article]:
        logger.info("Scraping source: %s", source_name)
        text, links = scrape_and_extract_text(url)
        article_links = self._find_articles(text, links)

        logger.info(
            "Found articles: %s", json.dumps(list(article_links.keys()), indent=2)
        )
        articles = []
        for title, article_url in article_links.items():
            if ArticleRepository.find_by_url(article_url):
                logger.info("Article already exists in the database")
                continue
            analysed_article = await self.analyse_article(title)
            logger.info(title)
            logger.info(f"is relevant?: {analysed_article.is_relevant}")
            logger.info(f"reason: {analysed_article.reason}")
            if not analysed_article.is_relevant:
                articles.append(Article(title=title, url=article_url))
                logger.info("---")
            else:
                summary = await self._summarize_article(article_url)
                articles.append(Article(title=title, url=article_url, summary=summary))
                logger.info("---")
        return articles

    @classmethod
    def find_url_by_title(cls, title_to_url: dict[str, str], title: str) -> str:
        for t, url in title_to_url.items():
            if title.lower() in t.lower():
                return url
        return ""

    @classmethod
    def _find_articles(cls, text: str, links: dict[str, str]) -> dict[str, str]:
        possible_titles = text.split("\n")
        title_link_pairs = (
            (title, cls.find_url_by_title(links, title)) for title in possible_titles
        )
        return {title: url for title, url in title_link_pairs if url}

    async def _summarize_article(self, article_url: str) -> str:
        logger.info("Summarizing article:", article_url)
        text, _ = scrape_and_extract_text(article_url)
        article = await self.summary_agent.run(text)
        return article.summary

    async def analyse_article(self, title) -> RelevantArticle:
        res = await self.interesting_article_agent.run(article_title=title)
        return res
