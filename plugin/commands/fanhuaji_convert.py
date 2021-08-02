from ..constant import HTTP_HEADERS
from ..constant import TEXT_DELIMITER
from ..functions import prepare_fanhuaji_convert_args
from ..libs import requests
from ..log import msg, print_msg
from ..settings import get_setting
from typing import Dict
import sublime
import sublime_plugin


class FanhuajiConvertCommand(sublime_plugin.TextCommand):
    def is_enabled(self) -> bool:
        return sum(map(len, self.view.sel())) > 0

    def is_visible(self) -> bool:
        return self.is_enabled()

    def run(self, edit: sublime.Edit, args: Dict = {}) -> None:
        real_args = prepare_fanhuaji_convert_args(self.view)
        real_args.update(args)

        try:
            result = self._do_api_convert(real_args)
        except requests.exceptions.ConnectionError as e:
            sublime.error_message(msg(f"Failed to reach the server: {e}"))
            return
        except requests.exceptions.RequestException as e:
            sublime.error_message(msg(f"Request exception: {e}"))
            return
        except ValueError as e:
            sublime.error_message(msg(f"Failed to decode the returned JSON: {e}"))
            return

        if int(result["code"]) != 0:
            sublime.error_message(msg(f'Error message from the server: {result["msg"]}'))
            return

        texts = result["data"]["text"].split(TEXT_DELIMITER)
        blocks = tuple({"region": z[0], "text": z[1]} for z in zip(self.view.sel(), texts))

        for block in reversed(blocks):
            self.view.replace(edit, block["region"], block["text"])

    def _do_api_convert(self, args: Dict) -> Dict:
        if get_setting("debug"):
            print_msg(f"Request with: {args}")

        url = get_setting("api_server") + "/convert"
        verify_ssl = bool(get_setting("ssl_cert_verification"))

        response = requests.post(url=url, data=args, headers=HTTP_HEADERS, verify=verify_ssl)

        return sublime.decode_value(response.text)
