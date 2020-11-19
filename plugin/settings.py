from functools import lru_cache
from typing import Any, Dict, List, Optional
import sublime


@lru_cache()
def get_package_name() -> str:
    """
    @brief Getsthe package name.

    @return The package name.
    """

    # anyway, the top module should always be the plugin name
    return __package__.partition(".")[0]


@lru_cache()
def get_package_path() -> str:
    return "Packages/" + get_package_name()


@lru_cache()
def get_settings_file() -> str:
    return get_package_name() + ".sublime-settings"


def get_settings_object() -> sublime.Settings:
    return sublime.load_settings(get_settings_file())


def get_setting(key: str, default: Optional[Any] = None) -> Any:
    return get_settings_object().get(key, default)


def get_text_delimiter() -> str:
    """
    The delimiter used to concat/split multiple selected text,
    so we could convert multiple text with only a single API call.

    This delimiter should be a extremely rarely used string.
    """

    return r"\n\5\9\8\n"


@lru_cache()
def get_converters_info(index: int) -> Dict[str, Any]:
    return get_all_converters_info()[index]


@lru_cache()
def get_all_converters_info() -> List[Dict[str, Any]]:
    return [
        {
            "name_api": "Simplified",
            "name_eng": "Simplified",
            "name_chi": "简体化",
            "desc": "将文字转换为简体。",
            "detail": "",
            "st_kind": (sublime.KIND_ID_MARKUP, "简", ""),
        },
        {
            "name_api": "Traditional",
            "name_eng": "Traditional",
            "name_chi": "繁體化",
            "desc": "將文字轉換為繁體。",
            "detail": "",
            "st_kind": (sublime.KIND_ID_MARKUP, "繁", ""),
        },
        {
            "name_api": "China",
            "name_eng": "China Localization",
            "name_chi": "中国化",
            "desc": "将文字转换为简体，并使用中国地区的词语修正。",
            "detail": "",
            "st_kind": (sublime.KIND_ID_MARKUP, "中", ""),
        },
        {
            "name_api": "Hongkong",
            "name_eng": "Hongkong Localization",
            "name_chi": "香港化",
            "desc": "將文字轉換為繁體，並使用香港地區的詞語修正。",
            "detail": "",
            "st_kind": (sublime.KIND_ID_MARKUP, "港", ""),
        },
        {
            "name_api": "Taiwan",
            "name_eng": "Taiwan Localization",
            "name_chi": "台灣化",
            "desc": "將文字轉換為繁體，並使用台灣地區的詞語修正。",
            "detail": "",
            "st_kind": (sublime.KIND_ID_MARKUP, "台", ""),
        },
        {
            "name_api": "Pinyin",
            "name_eng": "Pinyin",
            "name_chi": "拼音化",
            "desc": "將文字轉為拼音。",
            "detail": "",
            "st_kind": (sublime.KIND_ID_MARKUP, "拼", ""),
        },
        {
            "name_api": "Bopomofo",
            "name_eng": "Bopomofo",
            "name_chi": "注音化",
            "desc": "將文字轉為注音。",
            "detail": "",
            "st_kind": (sublime.KIND_ID_MARKUP, "注", ""),
        },
        {
            "name_api": "Mars",
            "name_eng": "Mars",
            "name_chi": "火星化",
            "desc": "將文字轉換為繁體火星文。",
            "detail": "",
            "st_kind": (sublime.KIND_ID_MARKUP, "火", ""),
        },
        {
            "name_api": "WikiSimplified",
            "name_eng": "Simplified (Wikipeida)",
            "name_chi": "维基简体化",
            "desc": "只使用维基百科的词库将文字转换为简体。",
            "detail": "一般而言，你应该用不到这个模式。",
            "st_kind": (sublime.KIND_ID_AMBIGUOUS, "简", ""),
        },
        {
            "name_api": "WikiTraditional",
            "name_eng": "Traditional (Wikipeida)",
            "name_chi": "維基繁體化",
            "desc": "只使用維基百科的詞庫將文字轉換為繁體。",
            "detail": "一般而言，你應該用不到這個模式。",
            "st_kind": (sublime.KIND_ID_AMBIGUOUS, "繁", ""),
        },
    ]
