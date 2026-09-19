"""Warnings shared by the temporary root-level compatibility entry points."""

import warnings


def warn_legacy_import(old: str, replacement: str) -> None:
    warnings.warn(
        f"{old} is deprecated; use {replacement}. "
        "See docs/entrypoint-migration.md for the compatibility window and examples.",
        DeprecationWarning,
        stacklevel=3,
    )
