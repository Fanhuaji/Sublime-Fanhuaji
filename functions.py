import json
import sublime
from .settings import get_setting, get_text_delimiter


def prepareFanhuajiConvertArgs(view: sublime.View) -> dict:
    args = get_setting("convert_params")

    # 轉換模組
    if "modules" in args and isinstance(args["modules"], dict):
        args["modules"] = json.dumps(args["modules"])

    # 轉換前取代
    if "userPreReplace" in args and isinstance(args["userPreReplace"], dict):
        args["userPreReplace"] = "\n".join(
            ["{}={}".format(_from, _to) for _from, _to in args["userPreReplace"].items()]
        )

    # 轉換後取代
    if "userPostReplace" in args and isinstance(args["userPostReplace"], dict):
        args["userPostReplace"] = "\n".join(
            ["{}={}".format(_from, _to) for _from, _to in args["userPostReplace"].items()]
        )

    # 保護字詞
    if "userProtectReplace" in args and isinstance(args["userProtectReplace"], list):
        args["userProtectReplace"] = "\n".join(args["userProtectReplace"])

    # 參數： API 全域
    args["apiKey"] = get_setting("api_key")
    args["prettify"] = False

    # 參數： API convert 端點
    args["text"] = get_text_delimiter().join([view.substr(region) for region in view.sel()])
    args["diffEnable"] = False

    return args
