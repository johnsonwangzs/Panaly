"""Frozen outputs from the original working-tree code, captured before migration."""

import hashlib
import json
from pathlib import Path

import pytest

from panaly.analysis import analyze_titles
from panaly.config import PROCEEDINGS, get_proceeding
from panaly.parsers import parse_titles
from panaly.paths import legacy_source_name, legacy_title_name
from panaly.plotting import create_wordcloud
from panaly.terminology import STOP_WORDS, TERMINOLOGY

FIXTURES = Path(__file__).parent / "fixtures"
ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((FIXTURES / "local_baseline.json").read_text(encoding="utf-8"))
PARSER_BASELINE = json.loads((FIXTURES / "parser_baseline.json").read_text(encoding="utf-8"))


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
    assert digest(STOP_WORDS) == BASELINE["stop_words_sha256"]


@pytest.mark.parametrize("case", PARSER_BASELINE, ids=lambda case: case["file"])
def test_parser_matches_original_fixture_output(case):
    content = (FIXTURES / case["file"]).read_text(encoding="utf-8")
    assert parse_titles(content, case["parser"]) == case["titles"]


@pytest.mark.local_data
@pytest.mark.parametrize(
    "case", BASELINE["proceedings"], ids=lambda case: f"{case['conference']}-{case['key']}"
)
def test_local_corpus_matches_original_titles_counts_ratios_and_wordcloud(case):
    path = ROOT / "resources" / case["source"]
    if not path.exists():
        pytest.skip("Original local source cache is not distributed with the repository")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == case["source_sha256"]
    proceeding = get_proceeding(case["conference"], case["key"])
    titles = parse_titles(path.read_text(encoding="utf-8"), proceeding.parser)
    assert len(titles) == case["total"]
    serialized = "".join(title + "\n" for title in titles).encode()
    assert hashlib.sha256(serialized).hexdigest() == case["titles_sha256"]
    for topic, keywords in BASELINE["keywords"].items():
        point = analyze_titles(proceeding, titles, keywords)
        assert point.count == case["counts"][topic]["count"], topic
        assert point.ratio == case["counts"][topic]["ratio"], topic
    # Raster placement is random; word identity, order, and weights are stable.
    assert list(create_wordcloud(titles).words_.items()) == list(case["wordcloud_words"].items())
