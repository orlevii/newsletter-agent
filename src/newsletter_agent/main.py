import asyncio
import random
from datetime import datetime
from pathlib import Path
from string import ascii_lowercase

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore[assignment]

if load_dotenv is not None:
    load_dotenv()


async def main():
    from newsletter_agent.agent import DailyUpdateAgent

    markdown = await DailyUpdateAgent().run()
    current = datetime.now().strftime("%Y-%m-%d")
    random_4_chars = [random.choice(ascii_lowercase) for _ in range(4)]
    random_4_chars_str = "".join(random_4_chars)
    Path(f"output-{current}-{random_4_chars_str}.md").write_text(markdown)


if __name__ == "__main__":
    asyncio.run(main())
