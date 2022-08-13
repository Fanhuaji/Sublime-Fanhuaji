from typing import Any, Dict

import sublime

from ..vendor import dacite, requests
from .constant import ST_PLATFORM_ARCH, ST_VERSION
from .log import print_msg
from .settings import get_setting
from .types import ApiConvertResponse, ConverterInfo

HTTP_HEADERS = {
    "user-agent": f"Sublime Text {ST_VERSION} ({ST_PLATFORM_ARCH}) Fanhuaji",
}


class FanhuajiApiUrl:
    @classmethod
    def base_url(cls) -> str:
        return get_setting("api_server").rstrip("/")

    @classmethod
    def convert(cls) -> str:
        return f"{cls.base_url()}/convert"

    @classmethod
    def service_info(cls) -> str:
        return f"{cls.base_url()}/service-info"


class Fanhuaji:
    CONVERTERS = (
        ConverterInfo(
            name_api="Simplified",
            name_eng="Simplified Chinese",
            name_chi="简体化",
            details="将文字转换为简体。",
            annotation="",
            st_kind=(sublime.KIND_ID_COLOR_ORANGISH, "简", ""),
        ),
        ConverterInfo(
            name_api="Traditional",
            name_eng="Traditional Chinese",
            name_chi="繁體化",
            details="將文字轉換為繁體。",
            annotation="",
            st_kind=(sublime.KIND_ID_COLOR_ORANGISH, "繁", ""),
        ),
        ConverterInfo(
            name_api="China",
            name_eng="China Localization",
            name_chi="中国化",
            details="将文字转换为简体，并使用中国地区的词语修正。",
            annotation="",
            st_kind=(sublime.KIND_ID_COLOR_CYANISH, "中", ""),
        ),
        ConverterInfo(
            name_api="Hongkong",
            name_eng="Hongkong Localization",
            name_chi="香港化",
            details="將文字轉換為繁體，並使用香港地區的詞語修正。",
            annotation="",
            st_kind=(sublime.KIND_ID_COLOR_CYANISH, "港", ""),
        ),
        ConverterInfo(
            name_api="Taiwan",
            name_eng="Taiwan Localization",
            name_chi="台灣化",
            details="將文字轉換為繁體，並使用台灣地區的詞語修正。",
            annotation="",
            st_kind=(sublime.KIND_ID_COLOR_CYANISH, "台", ""),
        ),
        ConverterInfo(
            name_api="Pinyin",
            name_eng="Pinyin",
            name_chi="拼音化",
            details="將文字轉為拼音。",
            annotation="",
            st_kind=(sublime.KIND_ID_COLOR_GREENISH, "拼", ""),
        ),
        ConverterInfo(
            name_api="Bopomofo",
            name_eng="Bopomofo",
            name_chi="注音化",
            details="將文字轉為注音。",
            annotation="",
            st_kind=(sublime.KIND_ID_COLOR_GREENISH, "注", ""),
        ),
        ConverterInfo(
            name_api="Mars",
            name_eng="Mars",
            name_chi="火星化",
            details="將文字轉換為繁體火星文。",
            annotation="",
            st_kind=(sublime.KIND_ID_COLOR_GREENISH, "火", ""),
        ),
        ConverterInfo(
            name_api="WikiSimplified",
            name_eng="Simplified Chinese (Wikipeida)",
            name_chi="维基简体化",
            details="只使用维基百科的词库将文字转换为简体。",
            annotation="（少用）",
            st_kind=(sublime.KIND_ID_COLOR_LIGHT, "简", ""),
        ),
        ConverterInfo(
            name_api="WikiTraditional",
            name_eng="Traditional Chinese (Wikipeida)",
            name_chi="維基繁體化",
            details="只使用維基百科的詞庫將文字轉換為繁體。",
            annotation="（少用）",
            st_kind=(sublime.KIND_ID_COLOR_LIGHT, "繁", ""),
        ),
    )

    TEXT_DELIMITER = r"\n\5\9\8\n"
    """
    The delimiter used to concat/split multiple selected text,
    so we could convert multiple text with only a single API call.
    This delimiter should be a extremely rarely used string.
    """

    @classmethod
    def convert(cls, args: Dict[str, Any]) -> ApiConvertResponse:
        if get_setting("debug"):
            print_msg(f"Request {args = }")

        try:
            response: requests.Response = requests.post(
                url=FanhuajiApiUrl.convert(),
                data=args,
                headers=HTTP_HEADERS,
                verify=bool(get_setting("ssl_cert_verification")),
            )
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError(f"Failed to reach the server: {e}") from e
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request exception: {e}") from e

        return dacite.from_dict(ApiConvertResponse, sublime.decode_value(response.text))
