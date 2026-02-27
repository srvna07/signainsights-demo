import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class DataReader:

    @staticmethod
    def load_yaml(path: str) -> dict:
        resolved = Path(path) if Path(path).is_absolute() else PROJECT_ROOT / path
        with open(resolved) as f:
            return yaml.safe_load(f)
