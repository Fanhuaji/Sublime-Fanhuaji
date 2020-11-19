from .. import st_features
from ..functions import prepare_fanhuaji_convert_args
from ..log import msg, print_msg
from ..settings import get_all_converters_info, get_converters_info, get_setting, get_text_delimiter
from typing import Dict, List, Union
import json
import requests
import sublime
import sublime_plugin

# HTTP headers used in issuing an API call
HTTP_HEADERS = {
    "user-agent": "Sublime Text {} Fanhuaji".format(st_features.ST_VERSION),
}


class FanhuajiConvertPanelCommand(sublime_plugin.WindowCommand):
    def run(self) -> None:
        trigger_format = "{name_eng} - {name_chi}"

        items = []  # type: List[Union[str, sublime.QuickPanelItem]]

        # use QuickPanelItem if possible
        if int(sublime.version()) >= 4083:
            items = [
                sublime.QuickPanelItem(
                    trigger=trigger_format.format_map(converter),
                    # details=converter["detail"],
                    annotation=converter["desc"],
                    kind=converter["st_kind"],
                )
                for converter in get_all_converters_info()
            ]
        else:
            # fmt: off
            items = [
                trigger_format.format_map(converter)
                for converter in get_all_converters_info()
            ]
            # fmt: on

        sublime.active_window().show_quick_panel(items, self.on_done)

    def on_done(self, index: int) -> None:
        if index == -1:
            return

        converter = get_converters_info(index)

        sublime.active_window().run_command(
            "fanhuaji_convert",
            {
                "args": {
                    "converter": converter["name_api"],
                },
            },
        )


class FanhuajiConvertCommand(sublime_plugin.TextCommand):
    def is_enabled(self, args: Dict = {}) -> bool:
        return sum([len(r) for r in self.view.sel()]) > 0

    def is_visible(self, args: Dict = {}) -> bool:
        return self.is_enabled(args)

    def run(self, edit: sublime.Edit, args: Dict = {}) -> None:
        real_args = prepare_fanhuaji_convert_args(self.view)
        real_args.update(args)

        try:
            result = self._do_api_convert(real_args)
        except requests.exceptions.ConnectionError as e:
            sublime.error_message(msg("Failed to reach the server: {}".format(e)))

            return
        except requests.exceptions.RequestException as e:
            sublime.error_message(msg("Request exception: {}".format(e)))

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

    def _do_api_convert(self, args: Dict) -> Dict:
        if get_setting("debug"):
            print_msg("Request with: {}".format(args))

        url = get_setting("api_server") + "/convert"
        verify_ssl = bool(get_setting("ssl_cert_verification"))

        response = requests.post(url=url, data=args, headers=HTTP_HEADERS, verify=verify_ssl)

        return json.loads(response.text)
