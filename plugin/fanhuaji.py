from typing import Any, Dict, Tuple

import sublime

from .constant import ST_PLATFORM_ARCH, ST_VERSION
from .libs import requests
from .log import print_msg
from .settings import get_setting
from .types import TD_ApiConvertResponse, TD_ConverterInfo

HTTP_HEADERS = {
    "user-agent": f"Sublime Text {ST_VERSION} ({ST_PLATFORM_ARCH}) Fanhuaji",
}


class Fanhuaji:
    converters: Tuple[TD_ConverterInfo, ...] = (
        {
            "name_api": "Simplified",
            "name_eng": "Simplified",
            "name_chi": "简体化",
            "details": "将文字转换为简体。",
            "annotation": "",
            "st_kind": (sublime.KIND_ID_COLOR_ORANGISH, "简", ""),
        },
        {
            "name_api": "Traditional",
            "name_eng": "Traditional",
            "name_chi": "繁體化",
            "details": "將文字轉換為繁體。",
            "annotation": "",
            "st_kind": (sublime.KIND_ID_COLOR_ORANGISH, "繁", ""),
        },
        {
            "name_api": "China",
            "name_eng": "China Localization",
            "name_chi": "中国化",
            "details": "将文字转换为简体，并使用中国地区的词语修正。",
            "annotation": "",
            "st_kind": (sublime.KIND_ID_COLOR_CYANISH, "中", ""),
        },
        {
            "name_api": "Hongkong",
            "name_eng": "Hongkong Localization",
            "name_chi": "香港化",
            "details": "將文字轉換為繁體，並使用香港地區的詞語修正。",
            "annotation": "",
            "st_kind": (sublime.KIND_ID_COLOR_CYANISH, "港", ""),
        },
        {
            "name_api": "Taiwan",
            "name_eng": "Taiwan Localization",
            "name_chi": "台灣化",
            "details": "將文字轉換為繁體，並使用台灣地區的詞語修正。",
            "annotation": "",
            "st_kind": (sublime.KIND_ID_COLOR_CYANISH, "台", ""),
        },
        {
            "name_api": "Pinyin",
            "name_eng": "Pinyin",
            "name_chi": "拼音化",
            "details": "將文字轉為拼音。",
            "annotation": "",
            "st_kind": (sublime.KIND_ID_COLOR_GREENISH, "拼", ""),
        },
        {
            "name_api": "Bopomofo",
            "name_eng": "Bopomofo",
            "name_chi": "注音化",
            "details": "將文字轉為注音。",
            "annotation": "",
            "st_kind": (sublime.KIND_ID_COLOR_GREENISH, "注", ""),
        },
        {
            "name_api": "Mars",
            "name_eng": "Mars",
            "name_chi": "火星化",
            "details": "將文字轉換為繁體火星文。",
            "annotation": "",
            "st_kind": (sublime.KIND_ID_COLOR_GREENISH, "火", ""),
        },
        {
            "name_api": "WikiSimplified",
            "name_eng": "Simplified (Wikipeida)",
            "name_chi": "维基简体化",
            "details": "只使用维基百科的词库将文字转换为简体。",
            "annotation": "（少用）",
            "st_kind": (sublime.KIND_ID_COLOR_LIGHT, "简", ""),
        },
        {
            "name_api": "WikiTraditional",
            "name_eng": "Traditional (Wikipeida)",
            "name_chi": "維基繁體化",
            "details": "只使用維基百科的詞庫將文字轉換為繁體。",
            "annotation": "（少用）",
            "st_kind": (sublime.KIND_ID_COLOR_LIGHT, "繁", ""),
        },
    )

    @classmethod
    def convert(cls, args: Dict[str, Any]) -> TD_ApiConvertResponse:
        if get_setting("debug"):
            print_msg(f"Request {args = }")

        url = get_setting("api_server") + "/convert"
        verify_ssl = bool(get_setting("ssl_cert_verification"))

        try:
            response = requests.post(url, data=args, headers=HTTP_HEADERS, verify=verify_ssl)
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError(f"Failed to reach the server: {e}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request exception: {e}")

        return sublime.decode_value(response.text)
