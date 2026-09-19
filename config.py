"""Deprecated compatibility imports; see docs/entrypoint-migration.md."""

from panaly._deprecation import warn_legacy_import
from panaly.compat import Config

__all__ = ["Config"]

warn_legacy_import("config.Config", "panaly.config, panaly.paths and panaly.terminology")
