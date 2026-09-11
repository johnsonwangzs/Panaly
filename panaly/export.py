"""Write auditable tables using the standard library."""

import csv
import json
from collections.abc import Iterable, Sequence
from datetime import datetime, timezone
from pathlib import Path

from panaly.analysis import KeywordMatcher
from panaly.models import TrendPoint
from panaly.normalize import NORMALIZATION_VERSION
from panaly.paths import report_paths
from panaly.terminology import TERMINOLOGY

SUMMARY_FIELDS = ("conference", "proceeding", "year", "keywords", "count", "total", "ratio_percent")
PAPER_FIELDS = (
    "conference",
    "proceeding",
    "year",
    "source_index",
    "original_title",
    "normalized_title",
    "matched_keywords",
    "source_url",
)
COMPARISON_FIELDS = (
    "conference",
    "proceeding",
    "keywords",
    "total",
    "legacy_count",
    "count",
    "delta",
    "added",
    "removed",
    "legacy_ratio_percent",
    "ratio_percent",
)
CHANGE_FIELDS = (
    "conference",
    "proceeding",
    "source_index",
    "change",
    "reason",
    "original_title",
    "legacy_title",
    "normalized_title",
    "legacy_matched_keywords",
    "matched_keywords",
    "source_url",
)


def write_csv(path: Path, fieldnames: Sequence[str], rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_trend(
    points: Sequence[TrendPoint],
    keywords: Sequence[str],
    description: str,
    output_dir: Path,
    source_hashes: dict[str, str],
    *,
    comparison_enabled: bool = False,
) -> dict[str, Path]:
    targets = report_paths(points[0].proceeding.conference, description, output_dir)
    summaries = []
    papers = []
    for point in points:
        item = point.proceeding
        summaries.append(
            {
                "conference": item.conference,
                "proceeding": item.key,
                "year": item.year,
                "keywords": json.dumps(list(keywords), ensure_ascii=False),
                "count": point.count,
                "total": point.total,
                "ratio_percent": point.ratio,
            }
        )
        for match in point.matches:
            papers.append(
                {
                    "conference": item.conference,
                    "proceeding": item.key,
                    "year": item.year,
                    "source_index": match.paper.source_index,
                    "original_title": match.paper.original_title,
                    "normalized_title": match.paper.normalized_title,
                    "matched_keywords": json.dumps(match.matched_keywords, ensure_ascii=False),
                    "source_url": item.url,
                }
            )
    write_csv(targets["summary"], SUMMARY_FIELDS, summaries)
    write_csv(targets["papers"], PAPER_FIELDS, papers)
    metadata = {
        "normalization_version": NORMALIZATION_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "description": description,
        "keywords": list(keywords),
        "normalized_queries": [
            {"keyword": label, "tokens": list(tokens)}
            for label, tokens in KeywordMatcher(keywords).queries
        ],
        "terminology": TERMINOLOGY,
        "sources": [
            {
                "conference": point.proceeding.conference,
                "proceeding": point.proceeding.key,
                "url": point.proceeding.url,
                "sha256": source_hashes[point.proceeding.key],
            }
            for point in points
        ],
        "summary_file": targets["summary"].name,
        "papers_file": targets["papers"].name,
        "comparison_enabled": comparison_enabled,
        "comparison_files": (
            [targets[name].name for name in ("comparison", "changes")] if comparison_enabled else []
        ),
    }
    targets["metadata"].write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return targets
