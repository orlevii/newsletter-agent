from pathlib import Path

import yaml
from pydantic import BaseModel

DEFAULT_GUIDELINES = """
* The article is about LLMs
"""


class Guidelines(BaseModel):
    relevance: str = DEFAULT_GUIDELINES
    summarization: str = ""


class Source(BaseModel):
    name: str
    url: str


class Config(BaseModel):
    guidelines: Guidelines = Guidelines()
    sources: list[Source] = []


def _read_config() -> Config:
    config_path = Path("config.yaml")
    if not config_path.is_file():
        return Config()
    with config_path.open() as f:
        conf = yaml.safe_load(f) or {}
    return Config(**conf)


config: Config = _read_config()
