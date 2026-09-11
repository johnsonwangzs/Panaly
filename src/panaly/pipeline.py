"""Compose collection, analysis, and plotting for CLI and Python callers."""

import logging
from collections.abc import Sequence
from pathlib import Path

from panaly.analysis import analyze_titles
from panaly.download import download_source
from panaly.models import Proceeding, TrendPoint
from panaly.parsers import parse_titles
from panaly.paths import Paths

logger = logging.getLogger(__name__)


def extract_titles(proceeding: Proceeding, paths: Paths) -> list[str]:
    content = paths.source_path(proceeding).read_text(encoding="utf-8")
    titles = parse_titles(content, proceeding.parser)
    target = paths.titles_path(proceeding)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(title + "\n" for title in titles), encoding="utf-8")
    logger.info("%s-%s: 提取 %s 篇标题", proceeding.conference, proceeding.key, len(titles))
    return titles


def prepare_titles(proceeding: Proceeding, paths: Paths) -> list[str]:
    download_source(proceeding, paths)
    return extract_titles(proceeding, paths)


def read_titles(proceeding: Proceeding, paths: Paths) -> list[str]:
    return paths.readable_titles_path(proceeding).read_text(encoding="utf-8").splitlines()


def run_trend(
    proceedings: Sequence[Proceeding],
    keywords: Sequence[str],
    description: str,
    paths: Paths = Paths(),
    *,
    show: bool = False,
) -> tuple[list[TrendPoint], Path]:
    from panaly.plotting import plot_trend

    if not proceedings or len({item.conference for item in proceedings}) != 1:
        raise ValueError("一次趋势分析需要同一个会议的一个或多个论文集。")
    points = [analyze_titles(item, prepare_titles(item, paths), keywords) for item in proceedings]
    target = plot_trend(points, description, paths.output_dir, show=show)
    return points, target


def run_wordcloud(
    proceeding: Proceeding,
    max_words: int = 150,
    paths: Paths = Paths(),
    *,
    show: bool = False,
) -> Path:
    from panaly.plotting import plot_wordcloud

    titles = prepare_titles(proceeding, paths)
    return plot_wordcloud(proceeding, titles, max_words, paths.output_dir, show=show)
