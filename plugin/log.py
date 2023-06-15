from __future__ import annotations

from .constant import PLUGIN_NAME


def msg(message: str) -> str:
    """
    Generate plugin message.

    :param      message:  The message

    :returns:   The plugin message.
    """

    return f"[{PLUGIN_NAME}] {message}"


def print_msg(message: str, show_message: bool = True) -> None:
    """
    Print plugin message to ST's console.

    :param      message:       The message
    :param      show_message:  Whether to print the message
    """

    if show_message:
        print(msg(message))
