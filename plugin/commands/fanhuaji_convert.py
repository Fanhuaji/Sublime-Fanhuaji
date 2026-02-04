from __future__ import annotations

from typing import override

import sublime
import sublime_plugin

from ..errors import FanhuajiError
from ..fanhuaji import Fanhuaji
from ..log import msg


class FanhuajiConvertCommand(sublime_plugin.TextCommand):
    @override
    def is_enabled(self) -> bool:
        return self.view.has_non_empty_selection_region()

    @override
    def is_visible(self) -> bool:
        return self.is_enabled()

    @override
    def run(self, edit: sublime.Edit, args: dict | None = None) -> None:
        convert_args = Fanhuaji.build_convert_args(self.view, args)

        try:
            result = Fanhuaji.convert(convert_args)
        except FanhuajiError as e:
            sublime.error_message(msg(str(e)))
            return

        if not result.is_ok:
            sublime.error_message(msg(f"Error message from the server: {result.msg}"))
            return

        for region, text in zip(
            reversed(self.view.sel()),
            reversed(result.data.text.split(Fanhuaji.TEXT_DELIMITER)),
        ):
            self.view.replace(edit, region, text)
