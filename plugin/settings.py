from typing import Any
from typing import overload

import sublime

from .constant import PLUGIN_NAME


def get_settings() -> sublime.Settings:
    return sublime.load_settings(f"{PLUGIN_NAME}.sublime-settings")


@overload
def get_setting(key: str) -> Any: ...
@overload
def get_setting(key: str, default: None) -> Any: ...
@overload
def get_setting[T](key: str, default: T) -> T: ...
def get_setting[T](key: str, default: T | None = None) -> T | None:
    return get_settings().get(key, default)
