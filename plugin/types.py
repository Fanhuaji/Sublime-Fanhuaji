from typing import Dict, List, Optional, Tuple, TypedDict


class TD_ConverterInfo(TypedDict):
    name_api: str  # like "WikiTraditional"
    name_eng: str  # like "Traditional (Wikipeida)"
    name_chi: str  # like "維基繁體化"
    details: str  # like "只使用維基百科的詞庫將文字轉換為繁體。"
    annotation: str  # like "（少用）"
    st_kind: Tuple[int, str, str]  # like (sublime.KIND_ID_AMBIGUOUS, "繁", "")


class TD_ApiRevisionInfo(TypedDict):
    build: str
    msg: str
    time: int


class TD_ApiBaseResponse(TypedDict):
    code: int
    msg: str
    revisions: TD_ApiRevisionInfo
    execTime: float


class TD_ApiConvertResponseData(TypedDict):
    converter: str
    text: str
    diff: Optional[str]
    jpTextStyles: List[str]
    usedModules: List[str]
    textFormat: str


class TD_ApiConvertResponse(TD_ApiBaseResponse):
    data: TD_ApiConvertResponseData


class TD_ApiConvertResponseDataConverterInfo(TypedDict):
    name: str
    desc: str
    cat: str


class TD_ApiConvertResponseDataModuleInfo(TypedDict):
    name: str
    desc: str
    cat: str
    isManual: bool


class TD_ApiServiceInfoResponseData(TypedDict):
    converters: Dict[str, TD_ApiConvertResponseDataConverterInfo]
    modules: Dict[str, TD_ApiConvertResponseDataModuleInfo]
    converterCategories: Dict[str, str]
    moduleCategories: Dict[str, str]
    textFormats: Dict[str, str]
    diffTemplates: Dict[str, str]
    allowEmptyApiKey: bool
    maxPostBodyBytes: int


class TD_ApiServiceInfoResponse(TD_ApiBaseResponse):
    data: TD_ApiServiceInfoResponseData
