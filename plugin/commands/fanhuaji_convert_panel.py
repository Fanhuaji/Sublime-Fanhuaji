from ..fanhuaji import Fanhuaji
import sublime
import sublime_plugin


class FanhuajiConvertPanelCommand(sublime_plugin.WindowCommand):
    def run(self) -> None:
        self.window.show_quick_panel(
            tuple(
                sublime.QuickPanelItem(
                    trigger="{name_eng} - {name_chi}".format_map(converter),
                    annotation=converter["annotation"],
                    details=converter["details"],
                    kind=converter["st_kind"],
                )
                for converter in Fanhuaji.converters
            ),
            self.on_done,
        )

    def on_done(self, index: int) -> None:
        if index == -1:
            return

        converter = Fanhuaji.converters[index]

        self.window.run_command(
            "fanhuaji_convert",
            {
                "args": {
                    "converter": converter["name_api"],
                },
            },
        )
