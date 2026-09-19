"""Deprecated compatibility imports; see docs/entrypoint-migration.md."""

from panaly._deprecation import warn_legacy_import
from panaly.compat import TendAnalyzer, analyze_tendency

__all__ = ["TendAnalyzer", "analyze_tendency"]

warn_legacy_import(
    "analyze_tendency", "panaly.analysis.analyze_papers and panaly.plotting.plot_trend"
)
