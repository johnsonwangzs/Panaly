"""Deprecated compatibility imports; see docs/entrypoint-migration.md."""

from panaly._deprecation import warn_legacy_import
from panaly.normalize import prepare_terminology

__all__ = ["prepare_terminology"]

warn_legacy_import("utils", "panaly.normalize")
