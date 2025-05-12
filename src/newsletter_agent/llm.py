from pydantic_ai.models.openai import OpenAIModel
from newsletter_agent.config import config


model = OpenAIModel(
    model_name=config.model_name, base_url=config.base_url, api_key="fake"
)
