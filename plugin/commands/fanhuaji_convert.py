from ..constant import TEXT_DELIMITER
from ..fanhuaji import Fanhuaji
from ..functions import prepare_fanhuaji_convert_args
from ..log import msg
from typing import Dict, Optional
import sublime
import sublime_plugin


class FanhuajiConvertCommand(sublime_plugin.TextCommand):
    def is_enabled(self) -> bool:
        return self.view.has_non_empty_selection_region()

    def is_visible(self) -> bool:
        return self.is_enabled()

    def run(self, edit: sublime.Edit, args: Optional[Dict] = None) -> None:
        args = prepare_fanhuaji_convert_args(self.view, args)

        try:
            result = Fanhuaji.convert(args)
        except Exception as e:
            sublime.error_message(msg(f"Failed to reach the server: {e}"))
            return

        if int(result["code"]) != 0:
            sublime.error_message(msg(f'Error message from the server: {result["msg"]}'))
            return

        texts = result["data"]["text"].split(TEXT_DELIMITER)
        region_text_pairs = tuple(zip(self.view.sel(), texts))

        for region, text in reversed(region_text_pairs):
            self.view.replace(edit, region, text)
