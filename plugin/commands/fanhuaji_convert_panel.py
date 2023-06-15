from __future__ import annotations

import sublime
import sublime_plugin

from ..fanhuaji import Fanhuaji


class FanhuajiConvertPanelCommand(sublime_plugin.WindowCommand):
    def run(self) -> None:
        self.window.show_quick_panel(
            tuple(
                sublime.QuickPanelItem(
                    trigger=f"{converter.name_eng} - {converter.name_chi}",
                    annotation=converter.annotation,
                    details=converter.details,
                    kind=converter.st_kind,
                )
                for converter in Fanhuaji.CONVERTERS
            ),
            self.on_done,
        )

    def on_done(self, index: int) -> None:
        if index == -1:
            return

        converter = Fanhuaji.CONVERTERS[index]

        self.window.run_command(
            "fanhuaji_convert",
            {
                "args": {
                    "converter": converter.name_api,
                },
            },
        )
