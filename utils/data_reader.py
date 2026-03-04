import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class DataReader:

    @staticmethod
    def load_yaml(path: str) -> dict:
        """
        Load configuration/test data from JSON files.
        Supports both .json and legacy .yaml/.yml extensions for backward compatibility.
        """
        resolved = Path(path) if Path(path).is_absolute() else PROJECT_ROOT / path

        # Handle file extension conversion
        if str(resolved).endswith(('.yaml', '.yml')):
            # Convert legacy .yaml/.yml paths to .json
            resolved = resolved.with_suffix('.json')

        with open(resolved) as f:
            return json.load(f)
