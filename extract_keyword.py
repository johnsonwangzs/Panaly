"""Deprecated experiment entry point; use python -m experiments.extract_keyword."""

from experiments.extract_keyword import KeywordExtractor, extract_keyword, main
from panaly._deprecation import warn_legacy_import

__all__ = ["KeywordExtractor", "extract_keyword"]

warn_legacy_import("extract_keyword", "experiments.extract_keyword")

if __name__ == "__main__":
    raise SystemExit(main())
