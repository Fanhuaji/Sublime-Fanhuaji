from collections import namedtuple
import json
import sublime
import sublime_plugin
import urllib

PLUGIN_NAME = __package__
PLUGIN_NAME_CHINESE = '繁化姬'
PLUGIN_DIR = 'Packages/%s' % PLUGIN_NAME
PLUGIN_SETTINGS = '%s.sublime-settings' % PLUGIN_NAME

# HTTP headers used in issuing an API call
HTTP_HEADERS = {
    'user-agent': 'Sublime Text Fanhuaji',
}

# the delimiter used to concat/split multiple selected text
# so we could convert multiple text with only a single API call
TEXT_DELIMITER = '\n\5\n'

RegionAndText = namedtuple('RegionAndText', ['region', 'text'])


def msg(msg):
    """
    @brief Format the message for this plugin.

    @param msg The message

    @return The formatted message
    """

    return '[{}] {}'.format(PLUGIN_NAME_CHINESE, msg)


class FanhuajiConvertCommand(sublime_plugin.TextCommand):
    def run(self, edit, args={}):
        v = self.view
        regions = v.sel()

        args = self._prepareArgs(args)

        try:
            result = self._doApiConvert(args)
        except urllib.error.HTTPError as e:
            sublime.error_message(msg('Failed to reach the server: {}'.format(e)))

            return
        except ValueError:
            sublime.error_message(msg('Failed to decode the returned JSON string...'))

            return

        if result['code'] != 0:
            sublime.error_message(msg('Error: {}'.format(result['msg'])))

            return

        texts = result['data']['text'].split(TEXT_DELIMITER)
        blocks = [RegionAndText._make(block) for block in zip(regions, texts)]

        for block in reversed(blocks):
            v.replace(edit, block.region, block.text)

    def _prepareArgs(self, args):
        settings = sublime.load_settings(PLUGIN_SETTINGS)
        v = self.view
        regions = v.sel()

        _args = settings.get('convert_params', {})

        # 轉換模組
        if 'modules' in _args and isinstance(_args['modules'], dict):
            _args['modules'] = json.dumps(_args['modules'])

        # 轉換前取代
        if 'userPreReplace' in _args and isinstance(_args['userPreReplace'], dict):
            _args['userPreReplace'] = '\n'.join([
                "{}={}".format(_from, _to)
                for _from, _to in _args['userPreReplace'].items()
            ])

        # 轉換後取代
        if 'userPostReplace' in _args and isinstance(_args['userPostReplace'], dict):
            _args['userPostReplace'] = '\n'.join([
                "{}={}".format(_from, _to)
                for _from, _to in _args['userPostReplace'].items()
            ])

        # 保護字詞
        if 'userProtectReplace' in _args and isinstance(_args['userProtectReplace'], list):
            _args['userProtectReplace'] = '\n'.join(_args['userProtectReplace'])

        # 參數： API 全域
        _args['apiKey'] = settings.get('api_key', '')
        _args['prettify'] = False

        # 參數： API convert 端點
        _args['text'] = TEXT_DELIMITER.join([v.substr(region) for region in regions])
        _args['diffEnable'] = False

        # args from ST command
        _args.update(args)

        return _args

    def _doApiConvert(self, args):
        settings = sublime.load_settings(PLUGIN_SETTINGS)

        if settings.get('debug', False):
            print(msg('Request with: {}'.format(args)))

        encoding = 'utf-8'
        url = settings.get('api_server') + '/convert'

        # prepare request
        data = urllib.parse.urlencode(args).encode(encoding)
        req = urllib.request.Request(url, data)
        for key, val in HTTP_HEADERS.items():
            req.add_header(key, val)

        # execute request
        with urllib.request.urlopen(req) as response:
            html = response.read().decode(encoding)

            return json.loads(html)
