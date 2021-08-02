from .constant import PLUGIN_NAME


def msg(message: str) -> str:
    """
    @brief Generate plugin message.

    @param message The message

    @return The plugin message.
    """

    return f"[{PLUGIN_NAME}] {message}"


def print_msg(message: str, show_message: bool = True) -> None:
    """
    @brief Print plugin message to ST's console.

    @param message      The message
    @param show_message Whether to print the message
    """

    if show_message:
        print(msg(message))
