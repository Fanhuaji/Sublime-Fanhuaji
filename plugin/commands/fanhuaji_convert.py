from typing import Any, Dict, Optional

import sublime
import sublime_plugin

from ..fanhuaji import Fanhuaji
from ..log import msg
from ..settings import get_setting


class FanhuajiConvertCommand(sublime_plugin.TextCommand):
    def is_enabled(self) -> bool:
        return self.view.has_non_empty_selection_region()

    def is_visible(self) -> bool:
        return self.is_enabled()

    def run(self, edit: sublime.Edit, args: Optional[Dict] = None) -> None:
        args = self._prepare_fanhuaji_convert_args(self.view, args)

        try:
            result = Fanhuaji.convert(args)
        except Exception as e:
            sublime.error_message(msg(str(e)))
            return

        if int(result.code) != 0:
            sublime.error_message(msg(f"Error message from the server: {result.msg}"))
            return

        for region, text in zip(
            reversed(self.view.sel()),
            reversed(result.data.text.split(Fanhuaji.TEXT_DELIMITER)),
        ):
            self.view.replace(edit, region, text)

    @staticmethod
    def _prepare_fanhuaji_convert_args(view: sublime.View, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        _args: Dict[str, Any] = get_setting("convert_params")

        # 轉換模組
        if "modules" in _args and isinstance(_args["modules"], dict):
            _args["modules"] = sublime.encode_value(_args["modules"])

        # 轉換前取代
        if "userPreReplace" in _args and isinstance(_args["userPreReplace"], dict):
            _args["userPreReplace"] = "\n".join(f"{old}={new}" for old, new in _args["userPreReplace"].items())

        # 轉換後取代
        if "userPostReplace" in _args and isinstance(_args["userPostReplace"], dict):
            _args["userPostReplace"] = "\n".join(f"{old}={new}" for old, new in _args["userPostReplace"].items())

        # 保護字詞
        if "userProtectReplace" in _args and isinstance(_args["userProtectReplace"], list):
            _args["userProtectReplace"] = "\n".join(_args["userProtectReplace"])

        # 參數： API 全域
        _args["apiKey"] = get_setting("api_key")
        _args["prettify"] = False

        # 參數： API convert 端點
        _args["text"] = Fanhuaji.TEXT_DELIMITER.join(view.substr(region) for region in view.sel())
        _args["diffEnable"] = False

        _args.update(args or {})

        return _args
