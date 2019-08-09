import json
import sublime
import sublime_plugin
import urllib
from .functions import prepareFanhuajiConvertArgs
from .log import msg, print_msg
from .settings import get_converters_info, get_setting, get_text_delimiter

# HTTP headers used in issuing an API call
HTTP_HEADERS = {"user-agent": "Sublime Text Fanhuaji"}


class FanhuajiConvertPanelCommand(sublime_plugin.WindowCommand):
    def run(self) -> None:
        w = sublime.active_window()

        converter_descs = [
            # fmt: off
            "{name} - {desc}".format(**converter)
            for converter in get_converters_info()
            # fmt: on
        ]

        w.show_quick_panel(converter_descs, self.on_done)

    def on_done(self, index: int) -> None:
        if index == -1:
            return

        w = sublime.active_window()

        converter = get_converters_info(index)

        w.run_command(
            # fmt: off
            "fanhuaji_convert",
            {
                "args": {
                    "converter": converter["name"],
                },
            }
            # fmt: on
        )


class FanhuajiConvertCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, args: dict = {}) -> None:
        v = self.view
        sels = v.sel()

        real_args = prepareFanhuajiConvertArgs(v)
        real_args.update(args)

        try:
            result = self._doApiConvert(real_args)
        except urllib.error.HTTPError as e:
            sublime.error_message(msg("Failed to reach the server: {}".format(e)))

            return
        except ValueError:
            sublime.error_message(msg("Failed to decode the returned JSON string..."))

            return

        if result["code"] != 0:
            sublime.error_message(msg("Error: {}".format(result["msg"])))

            return

        texts = result["data"]["text"].split(get_text_delimiter())
        blocks = [{"region": z[0], "text": z[1]} for z in zip(sels, texts)]

        for block in reversed(blocks):
            v.replace(edit, block["region"], block["text"])

    def _doApiConvert(self, args: dict) -> None:
        if get_setting("debug"):
            print_msg("Request with: {}".format(args))

        encoding = "utf-8"
        url = get_setting("api_server") + "/convert"

        # prepare request
        data = urllib.parse.urlencode(args).encode(encoding)
        req = urllib.request.Request(url, data)
        for key, val in HTTP_HEADERS.items():
            req.add_header(key, val)

        # execute request
        with urllib.request.urlopen(req) as response:
            html = response.read().decode(encoding)

            return json.loads(html)
