"""Keep original evidence and separately verify the reviewed phase-two results."""

import hashlib
import json
from pathlib import Path

import pytest

from panaly.analysis import analyze_papers
from panaly.comparison import LEGACY_TERMINOLOGY, compare_papers, legacy_normalize_title
from panaly.config import PROCEEDINGS, get_proceeding
from panaly.parsers import parse_papers
from panaly.paths import legacy_source_name, legacy_title_name
from panaly.plotting import create_wordcloud
from panaly.terminology import STOP_WORDS, TERMINOLOGY

FIXTURES = Path(__file__).parent / "fixtures"
ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((FIXTURES / "local_baseline.json").read_text(encoding="utf-8"))
PARSER_BASELINE = json.loads((FIXTURES / "parser_baseline.json").read_text(encoding="utf-8"))
CURRENT = json.loads((FIXTURES / "phase2_baseline.json").read_text(encoding="utf-8"))
CURRENT_PARSERS = json.loads((FIXTURES / "phase2_parser_baseline.json").read_text(encoding="utf-8"))


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def test_all_original_configuration_is_preserved():
    entries = [
        {
            "conference": conference,
            "key": key,
            "url": item.url,
            "parser": item.parser,
            "source": legacy_source_name(item),
            "title": legacy_title_name(item),
        }
        for conference, items in PROCEEDINGS.items()
        for key, item in items.items()
    ]
    assert len(entries) == 89
    assert digest(entries) == BASELINE["catalogue_sha256"]
    assert digest(list(TERMINOLOGY.items())) == BASELINE["terminology_sha256"]
    assert digest(list(LEGACY_TERMINOLOGY.items())) == BASELINE["terminology_sha256"]
    assert digest(STOP_WORDS) == BASELINE["stop_words_sha256"]


@pytest.mark.parametrize("case", PARSER_BASELINE, ids=lambda case: case["file"])
def test_parser_preserves_original_text_and_keeps_both_rule_baselines(case):
    content = (FIXTURES / case["file"]).read_text(encoding="utf-8")
    papers = parse_papers(content, case["parser"])
    current = next(item for item in CURRENT_PARSERS if item["file"] == case["file"])
    assert [paper.original_title for paper in papers] == current["original_titles"]
    assert [paper.normalized_title for paper in papers] == current["titles"]
    assert [legacy_normalize_title(p.original_title, case["parser"]) for p in papers] == case[
        "titles"
    ]


@pytest.mark.local_data
@pytest.mark.parametrize(
    "case", BASELINE["proceedings"], ids=lambda case: f"{case['conference']}-{case['key']}"
)
def test_local_corpus_reproduces_old_results_and_reviewed_new_counts(case):
    path = ROOT / "resources" / case["source"]
    if not path.exists():
        pytest.skip("Original local source cache is not distributed with the repository")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == case["source_sha256"]
    proceeding = get_proceeding(case["conference"], case["key"])
    papers = parse_papers(path.read_bytes().decode("utf-8"), proceeding.parser)
    current = next(
        row
        for row in CURRENT["proceedings"]
        if row["conference"] == case["conference"] and row["key"] == case["key"]
    )
    assert len(papers) == case["total"] == current["total"]
    old_titles = [legacy_normalize_title(p.original_title, proceeding.parser) for p in papers]
    serialized = "".join(title + "\n" for title in old_titles).encode()
    assert hashlib.sha256(serialized).hexdigest() == case["titles_sha256"]
    new_serialized = "".join(p.normalized_title + "\n" for p in papers).encode()
    assert hashlib.sha256(new_serialized).hexdigest() == current["titles_sha256"]
    originals = json.dumps([p.original_title for p in papers], ensure_ascii=False).encode()
    assert hashlib.sha256(originals).hexdigest() == current["original_titles_sha256"]
    for topic, keywords in BASELINE["keywords"].items():
        point = analyze_papers(proceeding, papers, keywords)
        assert point.count == current["counts"][topic]["count"], topic
        assert point.ratio == current["counts"][topic]["ratio"], topic
        summary, changes = compare_papers(proceeding, papers, keywords)
        assert summary["legacy_count"] == case["counts"][topic]["count"], topic
        assert summary["legacy_ratio_percent"] == case["counts"][topic]["ratio"], topic
        assert summary["delta"] == summary["added"] - summary["removed"]
        assert len(changes) == summary["added"] + summary["removed"]
    # Raster placement is random; word identity, order, and weights are stable.
    assert list(create_wordcloud(old_titles).words_.items()) == list(
        case["wordcloud_words"].items()
    )
