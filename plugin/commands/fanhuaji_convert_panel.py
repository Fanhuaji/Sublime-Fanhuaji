from typing import override

import sublime
import sublime_plugin

from ..converters import FANHUAJI_CONVERTERS


class FanhuajiConvertPanelCommand(sublime_plugin.WindowCommand):
    @override
    def run(self) -> None:
        self.window.show_quick_panel(
            tuple(
                sublime.QuickPanelItem(
                    trigger=f"{converter.name_eng} - {converter.name_chi}",
                    annotation=converter.annotation,
                    details=converter.details,
                    kind=converter.st_kind,
                )
                for converter in FANHUAJI_CONVERTERS
            ),
            self.on_done,
        )

    def on_done(self, index: int) -> None:
        if index == -1:
            return

        converter = FANHUAJI_CONVERTERS[index]

        self.window.run_command(
            "fanhuaji_convert",
            {
                "args": {
                    "converter": converter.name_api,
                },
            },
        )
