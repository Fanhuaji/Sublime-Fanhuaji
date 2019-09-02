import json
import sublime
from typing import Any, Dict
from .settings import get_setting, get_text_delimiter


def prepare_fanhuaji_convert_args(view: sublime.View) -> Dict[str, Any]:
    args = get_setting("convert_params")  # type: Dict[str, Any]

    # 轉換模組
    if "modules" in args and isinstance(args["modules"], dict):
        args["modules"] = json.dumps(args["modules"])

    # 轉換前取代
    if "userPreReplace" in args and isinstance(args["userPreReplace"], dict):
        args["userPreReplace"] = "\n".join(
            ["{}={}".format(from_, to_) for from_, to_ in args["userPreReplace"].items()]
        )

    # 轉換後取代
    if "userPostReplace" in args and isinstance(args["userPostReplace"], dict):
        args["userPostReplace"] = "\n".join(
            ["{}={}".format(from_, to_) for from_, to_ in args["userPostReplace"].items()]
        )

    # 保護字詞
    if "userProtectReplace" in args and isinstance(args["userProtectReplace"], list):
        args["userProtectReplace"] = "\n".join(args["userProtectReplace"])

    # 參數： API 全域
    args["apiKey"] = get_setting("api_key")
    args["prettify"] = False

    # 參數： API convert 端點
    args["text"] = get_text_delimiter().join(
        [
            view.substr(region) for region in view.sel()  # type: ignore
        ]
    )
    args["diffEnable"] = False

    return args
