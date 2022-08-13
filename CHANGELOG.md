# Fanhuaji （繁化姬）

## 2.0.4

- refactor: utilize `dataclass` and `dacite`

## 2.0.3

- fix: modules should be reloaded when update plugin
- refactor: simplify `boot.py`

## 2.0.2

- refactor: entity-ize server responses
- chore: update dependencies

## 2.0.1

- chore: update dependencies

## 2.0.0

- refactor: drop ST 3 support (min requirement is ST 4105)

  People can still use the legacy `1.3.3` release, which supports ST 3.

## 1.3.3

- fix: `fanhuaji_convert_panel` is not working
- chore: add a default keybinding for the `fanhuaji_convert_panel` command

  ```js
  [
    {
      keys: ["alt+f", "alt+h", "alt+j"],
      command: "fanhuaji_convert_panel",
    }
  ]
  ```

## 1.3.2

- feat: use `sublime.QuickPanelItem()` if possible

  This will require ST >= 4083.

## 1.3.1

- fix: typing dependency for ST 4

## 1.3.0

- fix: temporarily always use Python 3.3

## 1.2.4

- feat: add settings to disable SSL cert verification

## 1.2.3

- fix: disable commands if there is no selected text

## 1.2.2

- Run under Python 3.8 in ST 4.

## 1.2.1

- Add source codes type hinting.
- Put menu-like files into `menus/`.
- Put `msg()` in `log.py` rather than `functions.py`.

## 1.2.0

- Add command: `fanhuaji_convert_panel`.

## 1.1.0

- Add `注音化` to the context menu.
- Use a new side-by-side window to edit settings.

## 1.0.2

- Fix a typo.

## 1.0.1

- Fix potential mis-replacement.

## 1.0.0

- Initial release.
