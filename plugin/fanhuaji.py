from __future__ import annotations

from typing import Any

import requests
import sublime
from requests import ConnectionError, RequestException

from .constant import ST_PLATFORM_ARCH, ST_VERSION
from .converters import FanhuajiEndpoint
from .data_types import ApiConvertResponse
from .errors import FanhuajiError
from .log import print_msg
from .settings import get_setting

HTTP_HEADERS = {
    "user-agent": f"Sublime Text {ST_VERSION} ({ST_PLATFORM_ARCH}) Fanhuaji",
}


def _serialize_replace_dict(d: dict[str, str]) -> str:
    """Serialize a key=value replacement dict into the API's newline-delimited format."""
    return "\n".join(f"{old}={new}" for old, new in d.items())


class Fanhuaji:
    TEXT_DELIMITER = r"\n\5\9\8\n"
    """
    The delimiter used to concat/split multiple selected text,
    so we could convert multiple text with only a single API call.
    This delimiter should be a extremely rarely used string.
    """

    @staticmethod
    def base_url() -> str:
        return get_setting("api_server").rstrip("/")

    @classmethod
    def url(cls, endpoint: FanhuajiEndpoint) -> str:
        return f"{cls.base_url()}/{endpoint}"

    @classmethod
    def build_convert_args(cls, view: sublime.View, args: dict[str, Any] | None = None) -> dict[str, Any]:
        args = args or {}
        pref_args: dict[str, Any] = get_setting("convert_params")

        # 轉換模組
        if "modules" in pref_args and isinstance(pref_args["modules"], dict):
            pref_args["modules"] = sublime.encode_value(pref_args["modules"])

        # 轉換前取代
        if "userPreReplace" in pref_args and isinstance(pref_args["userPreReplace"], dict):
            pref_args["userPreReplace"] = _serialize_replace_dict(pref_args["userPreReplace"])

        # 轉換後取代
        if "userPostReplace" in pref_args and isinstance(pref_args["userPostReplace"], dict):
            pref_args["userPostReplace"] = _serialize_replace_dict(pref_args["userPostReplace"])

        # 保護字詞
        if "userProtectReplace" in pref_args and isinstance(pref_args["userProtectReplace"], list):
            pref_args["userProtectReplace"] = "\n".join(pref_args["userProtectReplace"])

        # 參數： API 全域
        pref_args["apiKey"] = get_setting("api_key")
        pref_args["prettify"] = False

        # 參數： API convert 端點
        pref_args["text"] = cls.TEXT_DELIMITER.join(view.substr(region) for region in view.sel())
        pref_args["diffEnable"] = False

        return pref_args | args

    @classmethod
    def convert(cls, args: dict[str, Any]) -> ApiConvertResponse:
        if get_setting("debug"):
            print_msg(f"Request {args = }")

        try:
            response = requests.post(
                url=cls.url(FanhuajiEndpoint.CONVERT),
                data=args,
                headers=HTTP_HEADERS,
                verify=bool(get_setting("ssl_cert_verification")),
            )
        except ConnectionError as e:
            raise FanhuajiError(f"Failed to reach the server: {e}") from e
        except RequestException as e:
            raise FanhuajiError(f"Request exception: {e}") from e

        return ApiConvertResponse.model_validate_json(response.content)
