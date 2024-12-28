from pydantic import BaseModel, Field
from pydantic_ai import Agent

from newsletter_agent.config import config


class SummarisedArticle(BaseModel):
    summary: str = Field(description="Short summary of the article")


SYSTEM_PROMPT = """
Summarize the following article in simple English.
{GUIDELINES}
""".strip()


class SummaryAgent:
    def __init__(self):
        self.agent = Agent(
            model="openai:gpt-4o-mini",
            system_prompt=SYSTEM_PROMPT.format(
                GUIDELINES=config.summarization_guidelines
            ).strip(),
            result_type=SummarisedArticle,
        )

    async def run(self, article: str) -> SummarisedArticle:
        data = await self.agent.run(user_prompt=article)
        return data.data
