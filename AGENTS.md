# CLAUDE.md

This file provides guidance to coding agents when working with code in this repository.

## Project Overview

Sublime Text plugin for [Fanhuaji (繁化姬)](https://zhconvert.org) — a Chinese text conversion service. The plugin calls the zhconvert.org REST API to convert selected text between Simplified/Traditional Chinese variants, Pinyin, Bopomofo, etc. It does **not** implement any conversion logic itself.

Primary branch: `st4`. Requires Sublime Text build 4201+ (Python 3.14).

## Development Commands

Dependencies are managed with `uv`. Install with:

```bash
make install-all    # all deps including dev
```

Linting and type checking (what CI runs):

```bash
make ci-check       # mypy + ruff lint + ruff format (check mode)
make ci-fix         # auto-fix ruff lint + format issues
make ci-fix-unsafe  # auto-fix including unsafe ruff fixes
```

Individual checks:

```bash
uv run --dev mypy -p plugin
uv run --dev ruff check --diff .
uv run --dev ruff format --diff .
```

There are no tests in this project. CI only runs linting (`make ci-check`).

## Architecture

```
boot.py                          # ST entry point: reloads plugin modules, imports plugin/*
plugin/
  __init__.py                    # plugin_loaded/plugin_unloaded hooks, re-exports commands
  commands/
    fanhuaji_convert.py          # FanhuajiConvertCommand (TextCommand) — converts selected text
    fanhuaji_convert_panel.py    # FanhuajiConvertPanelCommand (WindowCommand) — quick panel picker
  fanhuaji.py                    # Fanhuaji class: API client, converter definitions (FANHUAJI_CONVERTERS)
  data_types.py                  # Pydantic models for API responses, ConverterInfo dataclass
  settings.py                    # Settings helpers (reads Fanhuaji.sublime-settings)
  constant.py                    # Plugin name, ST version/platform constants
  log.py                         # Logging helpers
```

**Key flow:** User triggers `fanhuaji_convert` (directly or via panel) → selected regions are joined with a delimiter → single POST to `/convert` API → response split back and regions replaced.

`boot.py` handles hot-reloading by purging `sys.modules` entries for the package before re-importing, which is standard for ST4 plugin development.

## Code Conventions

- Python 3.14+ features are used (generics syntax `class Foo[T]`, `StrEnum`, `override`; no `from __future__ import annotations` needed — PEP 649 is default)
- Pydantic v2 for API response validation (`model_validate_json`)
- Ruff for linting (rules: E, F, W, I, UP, FURB, SIM) and formatting; line length 120
- mypy with `strict_optional` and `check_untyped_defs`; type stubs in `typings/`
- Runtime dependencies are declared in both `pyproject.toml` (for dev) and `dependencies.json` (for Package Control's dependency system)

## Approach

- Think before acting. Read existing files before writing code.
- Be concise in output but thorough in reasoning.
- Prefer editing over rewriting whole files.
- Do not re-read files you have already read unless the file may have changed.
- Test your code before declaring done.
- No sycophantic openers or closing fluff.
- Keep solutions simple and direct.
- User instructions always override this file.
