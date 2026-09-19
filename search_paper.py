"""Deprecated compatibility imports; see docs/entrypoint-migration.md."""

from panaly._deprecation import warn_legacy_import
from panaly.compat import PaperSearcher, search_paper

__all__ = ["PaperSearcher", "search_paper"]

warn_legacy_import("search_paper", "panaly.pipeline.read_papers and panaly.analysis.analyze_papers")
