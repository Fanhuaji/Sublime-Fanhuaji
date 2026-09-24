from pathlib import Path


def reload_plugin() -> None:
    import sys

    # remove all previously loaded plugin modules
    prefix = f"{__package__}."
    for module_name in tuple(filter(lambda m: m.startswith(prefix) and m != __name__, sys.modules)):
        del sys.modules[module_name]


def bypass_pydantic_version_check() -> None:
    """A workaround for https://github.com/jfcherng-sublime/ST-AutoSetSyntax/issues/36"""
    try:
        import package_control
    except ImportError:
        return

    pydantic_file = Path(package_control.__file__).parent / "pydantic/version.py"
    data = pydantic_file.read_bytes()
    data = data.replace(
        b"def check_pydantic_core_version() -> bool:",
        b"def  check_pydantic_core_version() -> bool:\n    return True",
        #     ^ intentional difference to avoid re-replacement next time
    )
    pydantic_file.write_bytes(data)


bypass_pydantic_version_check()
reload_plugin()

from .plugin import *  # ruff:ignore[undefined-local-with-import-star]
