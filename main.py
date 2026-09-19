"""Compatibility launcher; prefer python -m panaly [command] [options]."""

from typing import TYPE_CHECKING

from panaly.cli import main

if TYPE_CHECKING:
    from panaly.compat import plot_tendency, plot_wordcloud

__all__ = ["plot_tendency", "plot_wordcloud"]


def __getattr__(name: str):
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from panaly import compat
    from panaly._deprecation import warn_legacy_import

    replacement = "run_trend" if name == "plot_tendency" else "run_wordcloud"
    warn_legacy_import(f"main.{name}", f"panaly.pipeline.{replacement}")
    return getattr(compat, name)


if __name__ == "__main__":
    raise SystemExit(main())
