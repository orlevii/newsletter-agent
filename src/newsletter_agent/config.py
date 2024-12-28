from pathlib import Path

import yaml
from pydantic import BaseModel

DEFAULT_GUIDELINES = """
* The article is about LLMs
* The article is about big AI companies like OpenAI, Anthropic, Google, Meta, etc...
* The article is about fundraising or acquisitions in the AI space
* The article is about prompt evaluations

## Example 1
Input:
Perplexity's Carbon integration will make it easier for enterprises to connect their data to AI search

Output:
{
  "reason": "The article is Perplexity's Carbon integration, that means the article does not meet the criteria",
  "is_relevant": false
}
"""


class Config(BaseModel):
    relevance_guidelines: str = DEFAULT_GUIDELINES
    summarization_guidelines: str = ""
    sources: dict[str, str] = {
        "venturebeat": "https://venturebeat.com/category/ai/",
        "techcrunch": "https://techcrunch.com/category/artificial-intelligence/",
        "huggingface": "https://huggingface.co/blog",
    }


def _read_config() -> Config:
    config_path = Path("config.yaml")
    if not config_path.is_file():
        return Config()
    with config_path.open() as f:
        conf = yaml.safe_load(f) or {}
    return Config(**conf)


config = _read_config()
