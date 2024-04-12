from __future__ import annotations

import sys
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel

_T = TypeVar("_T")

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:

    class StrEnum(str, Enum):
        __str__ = str.__str__  # type: ignore
        __format__ = str.__format__  # type: ignore


@dataclass
class ConverterInfo:
    st_kind: tuple[int, str, str]
    """E.g., `(sublime.KIND_ID_AMBIGUOUS, "繁", "")`."""
    name_api: str
    """E.g., `"WikiTraditional"`."""
    name_eng: str
    """E.g., `"Traditional (Wikipeida)"`."""
    name_chi: str
    """E.g., `"維基繁體化"`."""
    details: str
    """E.g., `"只使用維基百科的詞庫將文字轉換為繁體。"`."""
    annotation: str = ""
    """E.g., `"（少用）"`."""


class ApiRevisionInfo(BaseModel):
    build: str
    msg: str
    time: int


class ApiResponseBase(BaseModel, Generic[_T], ABC):
    """This class describes the base API response."""

    code: int
    msg: str
    revisions: ApiRevisionInfo
    execTime: float
    data: _T

    @property
    def is_ok(self) -> bool:
        return self.code == 0


class ApiConvertResponseData(BaseModel):
    converter: str
    text: str
    diff: str | None
    jpTextStyles: list[str]
    usedModules: list[str]
    textFormat: str


class ApiConvertResponse(ApiResponseBase[ApiConvertResponseData]):
    """API response of `/convert`."""


class ApiConvertResponseDataConverterInfo(BaseModel):
    name: str
    desc: str
    cat: str


class ApiConvertResponseDataModuleInfo(BaseModel):
    name: str
    desc: str
    cat: str
    isManual: bool


class ApiServiceInfoResponseData(BaseModel):
    converters: dict[str, ApiConvertResponseDataConverterInfo]
    modules: dict[str, ApiConvertResponseDataModuleInfo]
    converterCategories: dict[str, str]
    moduleCategories: dict[str, str]
    textFormats: dict[str, str]
    diffTemplates: dict[str, str]
    allowEmptyApiKey: bool
    maxPostBodyBytes: int


class ApiServiceInfoResponse(ApiResponseBase[ApiServiceInfoResponseData]):
    """API response of `/service-info`."""
