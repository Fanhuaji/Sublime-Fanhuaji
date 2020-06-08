# Sublime-Fanhuaji （繁化姬）

[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/Fanhuaji/Sublime-Fanhuaji/Main/master?style=flat-square)](https://github.com/Fanhuaji/Sublime-Fanhuaji/actions)
[![Package Control](https://img.shields.io/packagecontrol/dt/Fanhuaji?style=flat-square)](https://packagecontrol.io/packages/Fanhuaji)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/Fanhuaji/Sublime-Fanhuaji?style=flat-square&logo=github)](https://github.com/Fanhuaji/Sublime-Fanhuaji/tags)
[![Project license](https://img.shields.io/github/license/Fanhuaji/Sublime-Fanhuaji?style=flat-square&logo=github)](https://github.com/Fanhuaji/Sublime-Fanhuaji/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Fanhuaji/Sublime-Fanhuaji?style=flat-square&logo=github)](https://github.com/Fanhuaji/Sublime-Fanhuaji/stargazers)
[![Donate to this project using Paypal](https://img.shields.io/badge/paypal-donate-blue.svg?style=flat-square&logo=paypal)](https://www.paypal.me/jfcherng/5usd)

本倉庫為[繁化姬](https://zhconvert.org)的 [Sublime Text 3](https://www.sublimetext.com) 插件。

## 安裝方式

- 使用 Package Control ：
  在 `Package Control` 中搜尋 `Fanhuaji` 安裝即可。

## 轉換模式

- 简体化：将文字转换为简体。
- 繁體化：將文字轉換為繁體。
- 中国化：将文字转换为简体，并使用中国地区的词语修正。
- 香港化：將文字轉換為繁體，並使用香港地區的詞語修正。
- 台灣化：將文字轉換為繁體，並使用台灣地區的詞語修正。
- 拼音化：將文字轉為拼音。
- 注音化：將文字轉為注音。
- 火星化：將文字轉換為繁體火星文。
- 维基简体化：只使用维基百科的词库将文字转换为简体。
- 維基繁體化：只使用維基百科的詞庫將文字轉換為繁體。

## 功能範例

![screenshot](https://raw.githubusercontent.com/Fanhuaji/Sublime-Fanhuaji/master/docs/images/convert_taiwan.gif)

## 插件設定

```javascript
{
    // 除錯模式
    "debug": false,
    // API 伺服器位址
    "api_server": "https://api.zhconvert.org",
    // API 金鑰（若無請留空）
    "api_key": "",
    // 將在 /convert API 端點使用的參數，請參考繁化姬說明文件 https://docs.zhconvert.org
    "convert_params": {/*
        "modules": {
            // 不要使用 "GanToZuo" 模組
            "GanToZuo": 0,
        },
        "userPostReplace": {
            // 轉換完成後再將 "哦" 轉換為 "喔"
            "哦": "喔",
        },
        "userProtectReplace": [
            // 保護 "內存" 不被轉換
            "內存",
        ],
    */},
}
```

## 商業使用

繁化姬的文字轉換服務在一般使用下為免費，但若是商業使用將酌收費用。
詳情請見[繁化姬商業使用](https://docs.zhconvert.org/commercial)。

## 錯誤回報

本插件僅使用繁化姬的網路 API ，並不實作文字轉換。
因此，如果您發現有「轉換錯誤」，請回報至以下任一位置。

- [繁化姬](https://zhconvert.org)
- [繁化姬 GitHub 討論頁](https://github.com/Fanhuaji/discussion/issues)
- [繁化姬 Telegram 群組](https://t.me/fanhuaji)

## 相關連結

- [繁化姬](https://zhconvert.org)
- [繁化姬 說明文件](https://docs.zhconvert.org)
