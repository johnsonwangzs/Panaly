"""Frozen phase-one matching, used only to explain changes to published counts."""

import json
import re
from collections.abc import Sequence
from pathlib import Path

from panaly.analysis import KeywordMatcher
from panaly.models import Paper, Parser, Proceeding

LEGACY_TERMINOLOGY = json.loads(
    Path(__file__).with_name("legacy_terms.json").read_text(encoding="utf-8")
)


def legacy_normalize_title(title: str, parser: Parser) -> str:
    if parser == "bibtex":
        title = re.sub(r"{(.*?)}", r"\1", title)
    title = re.sub(r"\s+", " ", title).lower()
    for canonical, variants in LEGACY_TERMINOLOGY.items():
        pattern = "|".join(re.escape(variant.lower()) for variant in variants)
        title = re.sub(pattern, " " + canonical + " ", title, flags=re.IGNORECASE)
    return title


def legacy_matched_keywords(title: str, keywords: Sequence[str]) -> tuple[str, ...]:
    tokens = re.sub(r"[^\w\s]", "", title.lower()).split()
    return tuple(keyword for keyword in dict.fromkeys(keywords) if keyword in tokens)


def compare_papers(
    proceeding: Proceeding, papers: Sequence[Paper], keywords: Sequence[str]
) -> tuple[dict, list[dict]]:
    matcher = KeywordMatcher(keywords)
    changes = []
    old_count = new_count = 0
    for paper in papers:
        old_title = legacy_normalize_title(paper.original_title, proceeding.parser)
        old_keywords = legacy_matched_keywords(old_title, keywords)
        new_keywords = matcher.match(paper.normalized_title)
        old_count += bool(old_keywords)
        new_count += bool(new_keywords)
        if bool(old_keywords) == bool(new_keywords):
            continue
        # Counterfactual: replace only title normalization and retain the old matcher.
        normalized_only = bool(legacy_matched_keywords(paper.normalized_title, keywords))
        reason = (
            "title_normalization"
            if normalized_only != bool(old_keywords)
            else "query_normalization_or_phrase"
        )
        changes.append(
            {
                "conference": proceeding.conference,
                "proceeding": proceeding.key,
                "source_index": paper.source_index,
                "change": "added" if new_keywords else "removed",
                "reason": reason,
                "original_title": paper.original_title,
                "legacy_title": old_title,
                "normalized_title": paper.normalized_title,
                "legacy_matched_keywords": json.dumps(old_keywords, ensure_ascii=False),
                "matched_keywords": json.dumps(new_keywords, ensure_ascii=False),
                "source_url": proceeding.url,
            }
        )
    total = len(papers)
    summary = {
        "conference": proceeding.conference,
        "proceeding": proceeding.key,
        "keywords": json.dumps(list(keywords), ensure_ascii=False),
        "total": total,
        "legacy_count": old_count,
        "count": new_count,
        "delta": new_count - old_count,
        "added": sum(row["change"] == "added" for row in changes),
        "removed": sum(row["change"] == "removed" for row in changes),
        "legacy_ratio_percent": old_count / total * 100 if total else float("nan"),
        "ratio_percent": new_count / total * 100 if total else float("nan"),
    }
    return summary, changes
