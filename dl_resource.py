"""Deprecated compatibility imports; see docs/entrypoint-migration.md."""

from panaly._deprecation import warn_legacy_import
from panaly.compat import Downloader, dl_resource

__all__ = ["Downloader", "dl_resource"]

warn_legacy_import("dl_resource", "panaly.download.download_source")
