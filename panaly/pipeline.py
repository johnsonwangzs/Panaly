"""Compose collection, analysis, and plotting for CLI and Python callers."""

import hashlib
import json
import logging
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from panaly.analysis import KeywordMatcher, analyze_papers
from panaly.download import download_source
from panaly.export import CHANGE_FIELDS, COMPARISON_FIELDS, export_trend, write_csv
from panaly.models import Paper, Proceeding, TrendPoint
from panaly.normalize import NORMALIZATION_VERSION
from panaly.parsers import paper_from_title, parse_papers
from panaly.paths import Paths

logger = logging.getLogger(__name__)


def extract_papers(proceeding: Proceeding, paths: Paths) -> list[Paper]:
    content = paths.source_path(proceeding).read_bytes()
    papers = parse_papers(content.decode("utf-8"), proceeding.parser)
    target = paths.titles_path(proceeding)
    target.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "schema_version": 1,
        "normalization_version": NORMALIZATION_VERSION,
        "conference": proceeding.conference,
        "proceeding": proceeding.key,
        "source_url": proceeding.url,
        "source_sha256": hashlib.sha256(content).hexdigest(),
        "papers": [asdict(paper) for paper in papers],
    }
    paths.papers_path(proceeding).write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    target.write_text("".join(paper.normalized_title + "\n" for paper in papers), encoding="utf-8")
    logger.info("%s-%s: 提取 %s 篇标题", proceeding.conference, proceeding.key, len(papers))
    return papers


def extract_titles(proceeding: Proceeding, paths: Paths) -> list[str]:
    return [paper.normalized_title for paper in extract_papers(proceeding, paths)]


def prepare_papers(proceeding: Proceeding, paths: Paths) -> list[Paper]:
    download_source(proceeding, paths)
    return extract_papers(proceeding, paths)


def prepare_titles(proceeding: Proceeding, paths: Paths) -> list[str]:
    return [paper.normalized_title for paper in prepare_papers(proceeding, paths)]


def read_papers(proceeding: Proceeding, paths: Paths) -> list[Paper]:
    source = paths.source_path(proceeding)
    if source.exists():
        return parse_papers(source.read_bytes().decode("utf-8"), proceeding.parser)
    cached = paths.papers_path(proceeding)
    if cached.exists():
        document = json.loads(cached.read_text(encoding="utf-8"))
        if (
            document.get("schema_version") != 1
            or document.get("conference") != proceeding.conference
            or document.get("proceeding") != proceeding.key
        ):
            raise ValueError(f"论文记录缓存与所选论文集不一致: {cached}")
        # Recompute normalization from the original title when terminology changes.
        return [
            paper_from_title(row["original_title"], row["source_index"], proceeding.parser)
            for row in document["papers"]
        ]
    raise FileNotFoundError(
        f"缺少 {proceeding.conference}/{proceeding.key} 的原始资源或论文记录。"
        "旧版 txt 只有标准化标题，无法还原原文；请先执行 trend 或 wordcloud。"
    )


def read_titles(proceeding: Proceeding, paths: Paths) -> list[str]:
    return [paper.normalized_title for paper in read_papers(proceeding, paths)]


def run_trend(
    proceedings: Sequence[Proceeding],
    keywords: Sequence[str],
    description: str,
    paths: Paths = Paths(),
    *,
    show: bool = False,
    compare_legacy: bool = False,
) -> tuple[list[TrendPoint], Path]:
    from panaly.plotting import plot_trend

    if not proceedings or len({item.conference for item in proceedings}) != 1:
        raise ValueError("一次趋势分析需要同一个会议的一个或多个论文集。")
    KeywordMatcher(keywords)  # Validate queries before touching the data directory.
    points = []
    source_hashes = {}
    comparisons, changes = [], []
    for item in proceedings:
        papers = prepare_papers(item, paths)
        points.append(analyze_papers(item, papers, keywords))
        document = json.loads(paths.papers_path(item).read_text(encoding="utf-8"))
        source_hashes[item.key] = document["source_sha256"]
        if compare_legacy:
            from panaly.comparison import compare_papers

            summary, changed_papers = compare_papers(item, papers, keywords)
            comparisons.append(summary)
            changes.extend(changed_papers)
    target = plot_trend(points, description, paths.output_dir, show=show)
    reports = export_trend(
        points,
        keywords,
        description,
        paths.output_dir,
        source_hashes,
        comparison_enabled=compare_legacy,
    )
    if compare_legacy:
        write_csv(reports["comparison"], COMPARISON_FIELDS, comparisons)
        write_csv(reports["changes"], CHANGE_FIELDS, changes)
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
