import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env", override=True)


def get_env() -> str:
    return os.getenv("ENV", "dev")
