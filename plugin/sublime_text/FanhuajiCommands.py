import json
import sublime
import sublime_plugin
from typing import Any, Dict
from urllib import error as url_error, request as url_request, parse as url_parse
from ..functions import prepare_fanhuaji_convert_args
from ..log import msg, print_msg
from ..settings import get_all_converters_info, get_converters_info, get_setting, get_text_delimiter

# HTTP headers used in issuing an API call
HTTP_HEADERS = {"user-agent": "Sublime Text Fanhuaji"}


class FanhuajiConvertPanelCommand(sublime_plugin.WindowCommand):
    def run(self) -> None:
        sublime.active_window().show_quick_panel(
            # fmt: off
            [
                "{name} - {desc}".format_map(converter)
                for converter in get_all_converters_info()
            ],
            # fmt: on
            self.on_done
        )

    def on_done(self, index: int) -> None:
        if index == -1:
            return

        converter = get_converters_info(index)

        sublime.active_window().run_command(
            "fanhuaji_convert",
            # fmt: off
            {
                "args": {
                    "converter": converter["name"],
                },
            },
            # fmt: on
        )


class FanhuajiConvertCommand(sublime_plugin.TextCommand):
    def is_enabled(self, args: Dict[str, Any] = {}) -> bool:
        return sum([len(r) for r in self.view.sel()]) > 0

    def is_visible(self, args: Dict[str, Any] = {}) -> bool:
        return self.is_enabled(args)

    def run(self, edit: sublime.Edit, args: Dict[str, Any] = {}) -> None:
        real_args = prepare_fanhuaji_convert_args(self.view)
        real_args.update(args)

        try:
            result = self._doApiConvert(real_args)
        except url_error.HTTPError as e:
            sublime.error_message(msg("Failed to reach the server: {}".format(e)))

            return
        except ValueError as e:
            sublime.error_message(msg("Failed to decode the returned JSON: {}".format(e)))

            return

        if int(result["code"]) != 0:
            sublime.error_message(msg("Error message from the server: {}".format(result["msg"])))

            return

        texts = result["data"]["text"].split(get_text_delimiter())
        blocks = [{"region": z[0], "text": z[1]} for z in zip(self.view.sel(), texts)]

        for block in reversed(blocks):
            self.view.replace(edit, block["region"], block["text"])

    def _doApiConvert(self, args: Dict[str, Any]) -> Dict[str, Any]:
        if get_setting("debug"):
            print_msg("Request with: {}".format(args))

        encoding = "utf-8"
        url = get_setting("api_server") + "/convert"

        # prepare request
        data = url_parse.urlencode(args).encode(encoding)
        req = url_request.Request(url, data)
        for key, val in HTTP_HEADERS.items():
            req.add_header(key, val)

        # execute request
        with url_request.urlopen(req) as response:
            html = response.read().decode(encoding)

            return json.loads(html)
