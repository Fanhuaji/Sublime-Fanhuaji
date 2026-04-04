import sys

import sublime

assert __package__

PLUGIN_NAME = __package__.partition(".")[0]
"""E.g., `"Fanhuaji"`."""

ST_ARCH = sublime.arch()
"""E.g., `"x64"`."""
ST_CHANNEL = sublime.channel()
"""E.g., `"dev"`."""
ST_PLATFORM = sublime.platform()
"""E.g., `"windows"`."""
ST_PLATFORM_ARCH = f"{ST_PLATFORM}_{ST_ARCH}"
"""E.g., `"windows_x64"`."""
ST_VERSION = int(sublime.version())
"""E.g., `4113`."""
PY_VERSION_FULL = sys.version
"""E.g., `"3.8.8 (default, Mar 10 2021, 13:30:47) [MSC v.1915 64 bit (AMD64)]"`."""
PY_VERSION = PY_VERSION_FULL.partition(" ")[0]
"""E.g., `"3.8.8"`."""
