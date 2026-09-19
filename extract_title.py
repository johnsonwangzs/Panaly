"""Deprecated compatibility imports; see docs/entrypoint-migration.md."""

from panaly._deprecation import warn_legacy_import
from panaly.compat import TitleExtractor, extract_title
from panaly.normalize import substitute_terminology

__all__ = ["TitleExtractor", "extract_title", "substitute_terminology"]

warn_legacy_import("extract_title", "panaly.pipeline, panaly.parsers and panaly.normalize")
