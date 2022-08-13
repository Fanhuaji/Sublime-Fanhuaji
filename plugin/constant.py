import sys

import sublime

PLUGIN_NAME = __package__.partition(".")[0]
"""Like `"AutoSetSyntax"`."""

ST_ARCH = sublime.arch()
"""Like `"x64"`."""
ST_CHANNEL = sublime.channel()
"""Like `"dev"`."""
ST_PLATFORM = sublime.platform()
"""Like `"windows"`."""
ST_PLATFORM_ARCH = f"{ST_PLATFORM}_{ST_ARCH}"
"""Like `"windows_x64"`."""
ST_VERSION = int(sublime.version())
"""Like `4113`."""
PY_VERSION_FULL = sys.version
"""Like `"3.8.8 (default, Mar 10 2021, 13:30:47) [MSC v.1915 64 bit (AMD64)]"`."""
PY_VERSION = PY_VERSION_FULL.partition(" ")[0]
"""Like `"3.8.8"`."""
