from typing import Tuple, TypedDict


class TD_ConverterInfo(TypedDict):
    name_api: str  # like "WikiTraditional"
    name_eng: str  # like "Traditional (Wikipeida)"
    name_chi: str  # like "維基繁體化"
    desc: str  # like "只使用維基百科的詞庫將文字轉換為繁體。"
    detail: str  # like "一般而言，你應該用不到這個模式。"
    st_kind: Tuple[int, str, str]  # like (sublime.KIND_ID_AMBIGUOUS, "繁", "")
