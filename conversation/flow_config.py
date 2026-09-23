import json
from pathlib import Path
from typing import Any, Dict


class ConversationFlowConfig:
    """
    Loads and provides access to conversation flow configuration.
    """

    def __init__(self, config_path=None):
        if config_path is None:
            config_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "conversation_flow_config.json"
            )

        self.config_path = Path(config_path)
        self.config = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Conversation config not found: {self.config_path}"
            )

        with self.config_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def get(self, *keys, default=None):
        """
        Safely retrieve a nested configuration value.
        """

        value = self.config

        for key in keys:
            if not isinstance(value, dict):
                return default

            value = value.get(key)

            if value is None:
                return default

        return value