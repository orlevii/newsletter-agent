from pydantic import BaseModel, Field
from pydantic_ai import Agent


class InterestingArticle(BaseModel):
    reason: str = Field(description="Reason why the article is interesting or not")
    is_interesting: bool = Field(
        description="Is the article interesting according to the guidelines"
    )


SYSTEM_PROMPT = """
Your task is to determine if the article is interesting enough for us.
The article is interesting if it fits one of the following criteria:
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
  "is_interesting": false
}

Respond with a JSON in the following format:
{
  "reason": "The article is about LLMs",
  "is_interesting": true
}
""".strip()


class InterestingArticleAgent:
    def __init__(self):
        self.agent = Agent(
            model="openai:gpt-4o-mini",
            system_prompt=SYSTEM_PROMPT,
            result_type=InterestingArticle,
        )

    async def run(self, article_title: str) -> InterestingArticle:
        data = await self.agent.run(user_prompt=article_title)
        return data.data
