from typing import TypeVar
from urllib.parse import ParseResult, urlparse

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed

from newsletter_agent.logger import logger

T = TypeVar("T")
MIN_WORDS = 5


@retry(wait=wait_fixed(10), stop=stop_after_attempt(3), after=logger.debug)
def make_request(url: str) -> str:
    headers = {
        "User-Agent": "curl/7.68.0"  # Adjust version to match your curl
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad HTTP responses
    return response.text


def create_links_map(soup: BeautifulSoup, base_url: ParseResult) -> dict[str, str]:
    text_to_link_map = {}

    links = list(soup.find_all("a", href=True))
    for a in links:
        text = a.get_text(strip=True)
        href = a["href"]
        text_to_link_map[text] = href
        if not href.startswith("http"):
            text_to_link_map[text] = f"{base_url.scheme}://{base_url.netloc}{href}"

    return text_to_link_map


def ordered_dedup(items: list[T]) -> list[T]:
    items_set = set()
    res = []
    for i in items:
        if i not in items_set:
            res.append(i)
            items_set.add(i)
    return res


def scrape_and_extract_text(url: str) -> tuple[str, dict[str, str]]:
    html_text = make_request(url)
    soup = BeautifulSoup(html_text, "html.parser")

    all_text = soup.get_text(separator="\n", strip=True)
    all_text_lines = all_text.split("\n")

    cleaned_text = [line for line in all_text_lines if line]
    cleaned_text = [line for line in cleaned_text if len(line.split()) > MIN_WORDS]
    cleaned_text = ordered_dedup(cleaned_text)

    text_to_link_map = create_links_map(soup, base_url=urlparse(url))
    return "\n".join(cleaned_text), text_to_link_map
