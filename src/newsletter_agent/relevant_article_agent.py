from pydantic import BaseModel, Field
from pydantic_ai import Agent

from newsletter_agent.config import config


class RelevantArticle(BaseModel):
    reason: str = Field(description="Reason why the article is interesting or not")
    is_relevant: bool = Field(
        description="Is the article relevant according to the guidelines"
    )


SYSTEM_PROMPT = """
Your task is to determine if the given article is relevant for us.
The article is relevant if it fits to one of the following guidelines:
{GUIDELINES}

Respond with a JSON in the following format:
{{
  "reason": "<reason>",
  "is_relevant": <true/false>
}}
""".strip()


class RelevantArticleAgent:
    def __init__(self):
        self.agent = Agent(
            model="openai:gpt-4o-mini",
            system_prompt=SYSTEM_PROMPT.format(GUIDELINES=config.relevance_guidelines),
            result_type=RelevantArticle,
        )

    async def run(self, article_title: str) -> RelevantArticle:
        data = await self.agent.run(user_prompt=article_title)
        return data.data
