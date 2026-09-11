"""Run directly from source: python main.py [command] [options]."""

from panaly.cli import main
from panaly.compat import plot_tendency, plot_wordcloud

__all__ = ["plot_tendency", "plot_wordcloud"]

if __name__ == "__main__":
    raise SystemExit(main())
