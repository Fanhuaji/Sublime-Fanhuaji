from .constant import PLUGIN_NAME
from typing import Any, Optional
import sublime


def get_settings() -> sublime.Settings:
    return sublime.load_settings(f"{PLUGIN_NAME}.sublime-settings")


def get_setting(key: str, default: Optional[Any] = None) -> Any:
    return get_settings().get(key, default)
