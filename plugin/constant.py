import sys

import sublime

PLUGIN_NAME = __package__.partition(".")[0]  # like "AutoSetSyntax"

ST_ARCH = sublime.arch()  # like "x64"
ST_CHANNEL = sublime.channel()  # like "dev"
ST_PLATFORM = sublime.platform()  # like "windows"
ST_PLATFORM_ARCH = f"{ST_PLATFORM}_{ST_ARCH}"  # like "windows_x64"
ST_VERSION = int(sublime.version())  # like 4113
PY_VERSION_FULL = sys.version  # like "3.8.8 (default, Mar 10 2021, 13:30:47) [MSC v.1915 64 bit (AMD64)]"
PY_VERSION = PY_VERSION_FULL.partition(" ")[0]  # like "3.8.8"

# The delimiter used to concat/split multiple selected text,
# so we could convert multiple text with only a single API call.
# This delimiter should be a extremely rarely used string.
TEXT_DELIMITER = r"\n\5\9\8\n"
