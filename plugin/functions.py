from .constant import TEXT_DELIMITER
from .constant import CONVERTERS_INFO
from .settings import get_setting
from .types import TD_ConverterInfo
from functools import lru_cache
from typing import Any, Dict
import sublime


@lru_cache()
def get_converter_info(index: int) -> TD_ConverterInfo:
    return CONVERTERS_INFO[index]


def prepare_fanhuaji_convert_args(view: sublime.View) -> Dict[str, Any]:
    args: Dict[str, Any] = get_setting("convert_params")

    # 轉換模組
    if "modules" in args and isinstance(args["modules"], dict):
        args["modules"] = sublime.encode_value(args["modules"])

    # 轉換前取代
    if "userPreReplace" in args and isinstance(args["userPreReplace"], dict):
        args["userPreReplace"] = "\n".join(f"{from_}={to_}" for from_, to_ in args["userPreReplace"].items())

    # 轉換後取代
    if "userPostReplace" in args and isinstance(args["userPostReplace"], dict):
        args["userPostReplace"] = "\n".join(f"{from_}={to_}" for from_, to_ in args["userPostReplace"].items())

    # 保護字詞
    if "userProtectReplace" in args and isinstance(args["userProtectReplace"], list):
        args["userProtectReplace"] = "\n".join(args["userProtectReplace"])

    # 參數： API 全域
    args["apiKey"] = get_setting("api_key")
    args["prettify"] = False

    # 參數： API convert 端點
    args["text"] = TEXT_DELIMITER.join(view.substr(region) for region in view.sel())
    args["diffEnable"] = False

    return args
