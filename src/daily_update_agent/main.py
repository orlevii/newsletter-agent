import asyncio
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore[assignment]

if load_dotenv is not None:
    load_dotenv()


async def main():
    from daily_update_agent.agent import DailyUpdateAgent

    markdown = await DailyUpdateAgent().run()
    Path("output.md").write_text(markdown)


if __name__ == "__main__":
    asyncio.run(main())
