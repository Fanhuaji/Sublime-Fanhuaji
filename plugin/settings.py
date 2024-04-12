from __future__ import annotations

from typing import Any, TypeVar, overload

import sublime

from .constant import PLUGIN_NAME

_T = TypeVar("_T")


def get_settings() -> sublime.Settings:
    return sublime.load_settings(f"{PLUGIN_NAME}.sublime-settings")


@overload
def get_setting(key: str) -> Any: ...
@overload
def get_setting(key: str, default: None) -> Any: ...
@overload
def get_setting(key: str, default: _T) -> _T: ...
def get_setting(key: str, default: _T | None = None) -> _T | None:
    return get_settings().get(key, default)
