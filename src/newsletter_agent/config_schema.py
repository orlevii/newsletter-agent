import json
from pathlib import Path

from newsletter_agent.config import Config


def main():
    schema = Config.model_json_schema()
    schema_file = Path("config_schema.json")
    with schema_file.open("w") as f:
        json.dump(schema, f, indent=2)


if __name__ == "__main__":
    main()
