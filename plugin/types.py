from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConverterInfo:
    name_api: str
    """Like `"WikiTraditional"`."""
    name_eng: str
    """Like `"Traditional (Wikipeida)"`."""
    name_chi: str
    """Like `"維基繁體化"`."""
    details: str
    """Like `"只使用維基百科的詞庫將文字轉換為繁體。"`."""
    annotation: str
    """Like `"（少用）"`."""
    st_kind: tuple[int, str, str]
    """Like `(sublime.KIND_ID_AMBIGUOUS, "繁", "")`."""


@dataclass
class ApiResponseBase:
    code: int
    msg: str
    revisions: ApiRevisionInfo
    execTime: float


@dataclass
class ApiRevisionInfo:
    build: str
    msg: str
    time: int


@dataclass
class ApiConvertResponse(ApiResponseBase):
    """Response of `/convert`."""

    data: ApiConvertResponseData


@dataclass
class ApiConvertResponseData:
    converter: str
    text: str
    diff: str | None
    jpTextStyles: list[str]
    usedModules: list[str]
    textFormat: str


@dataclass
class ApiServiceInfoResponse(ApiResponseBase):
    """Response of `/service-info`."""

    data: ApiServiceInfoResponseData


@dataclass
class ApiServiceInfoResponseData:
    converters: dict[str, ApiConvertResponseDataConverterInfo]
    modules: dict[str, ApiConvertResponseDataModuleInfo]
    converterCategories: dict[str, str]
    moduleCategories: dict[str, str]
    textFormats: dict[str, str]
    diffTemplates: dict[str, str]
    allowEmptyApiKey: bool
    maxPostBodyBytes: int


@dataclass
class ApiConvertResponseDataConverterInfo:
    name: str
    desc: str
    cat: str


class ApiConvertResponseDataModuleInfo:
    name: str
    desc: str
    cat: str
    isManual: bool
