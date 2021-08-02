from ..settings import get_converters_info
from ..settings import get_converter_info
from typing import Tuple, Union
import sublime
import sublime_plugin


class FanhuajiConvertPanelCommand(sublime_plugin.WindowCommand):
    def run(self) -> None:
        trigger_format = "{name_eng} - {name_chi}"

        items: Tuple[Union[str, sublime.QuickPanelItem], ...] = tuple(
            sublime.QuickPanelItem(
                trigger=trigger_format.format_map(converter),
                # details=converter["detail"],
                annotation=converter["desc"],
                kind=converter["st_kind"],
            )
            for converter in get_converters_info()
        )

        self.window.show_quick_panel(items, self.on_done)

    def on_done(self, index: int) -> None:
        if index == -1:
            return

        converter = get_converter_info(index)

        self.window.run_command(
            "fanhuaji_convert",
            {
                "args": {
                    "converter": converter["name_api"],
                },
            },
        )
