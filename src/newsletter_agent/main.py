import asyncio
import json
from datetime import datetime
from pathlib import Path

from newsletter_agent.config import config
from newsletter_agent.logger import logger

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore[assignment]

if load_dotenv is not None:
    load_dotenv()


async def main() -> None:
    from newsletter_agent.agent import DailyUpdateAgent

    logger.debug("Config: %s", json.dumps(config.model_dump(), indent=2))

    markdown = await DailyUpdateAgent().run()
    current = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_path = Path(f"output-{current}.md")
    logger.info("Writing output to %s", output_path)
    output_path.write_text(markdown)


if __name__ == "__main__":
    asyncio.run(main())
