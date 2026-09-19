"""Deprecated compatibility imports; see docs/entrypoint-migration.md."""

from panaly._deprecation import warn_legacy_import
from panaly.compat import gen_wordcloud

__all__ = ["gen_wordcloud"]

warn_legacy_import(
    "gen_wordcloud", "panaly.plotting.plot_wordcloud or panaly.pipeline.run_wordcloud"
)
