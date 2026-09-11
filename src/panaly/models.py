"""Data shared by collection, analysis, and plotting."""

from dataclasses import dataclass
from typing import Literal

Parser = Literal["bibtex", "acl_html", "downloads_html", "nips_html"]


@dataclass(frozen=True)
class Proceeding:
    conference: str
    key: str
    url: str
    parser: Parser

    @property
    def year(self) -> int:
        return int(self.key[:4])

    @property
    def track(self) -> str:
        return self.key[4:]

    @property
    def suffix(self) -> str:
        return ".bib" if self.parser == "bibtex" else ".html"


@dataclass(frozen=True)
class TrendPoint:
    proceeding: Proceeding
    count: int
    total: int

    @property
    def ratio(self) -> float:
        # Preserve the previous NumPy result for an empty proceeding.
        return self.count / self.total * 100.0 if self.total else float("nan")
