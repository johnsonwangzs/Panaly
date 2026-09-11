import math

import pytest

from panaly.analysis import KeywordMatcher, analyze_titles, find_matches
from panaly.comparison import compare_papers
from panaly.config import get_proceeding
from panaly.normalize import normalize_title
from panaly.parsers import paper_from_title


@pytest.mark.parametrize(
    "title, query, expected",
    [
        ("Large Language Models", "LLM", True),
        ("LLMs", "large-language-model", True),
        ("language models", "LM", True),
        ("Large Language Models", "language model", False),
        ("Graph-based knowledge", "graph", True),
        ("graph_based learning", "graph based", True),
        ("graph based learning", "graph learning", False),
        ("knowledge graphs", "Knowledge Graphs", True),
        ("knowledge graphs", "knowledge graph", False),
        ("multi–agent reasoning", "agents", True),
        ("ＬＬＭ-based generation", "llm", True),
        ("LLM/LM comparisons", "lm", True),
        ("chemical reagents", "agent", False),
        ("Allman and sLLM", "llm", False),
        ("knowledgeable models", "knowledge", False),
    ],
)
def test_keyword_boundaries_aliases_and_phrases(title, query, expected):
    assert bool(find_matches([title], [query])) is expected


def test_a_paper_counts_once_and_records_matching_queries():
    item = get_proceeding("acl", "2025mainlong")
    titles = ["LLMs, LLMs and knowledge", "Knowledge", "Other"]
    point = analyze_titles(item, titles, ["LLM", "large language models", "knowledge"])
    assert (point.count, point.total) == (2, 3)
    assert point.matches[0].matched_keywords == ("LLM", "knowledge")
    assert point.matches[0].paper.original_title == titles[0]
    assert point.matches[1].matched_keywords == ("knowledge",)


@pytest.mark.parametrize("keywords", [[], [""], ["---"], ["knowledge", " "]])
def test_empty_queries_are_rejected(keywords):
    with pytest.raises(ValueError):
        KeywordMatcher(keywords)


def test_normalization_is_idempotent_and_preserves_canonical_term_names():
    title = "Large Language Models and language models with Chain-of-Thought"
    normalized = normalize_title(title)
    assert normalized == "LLM and LM with CoT"
    assert normalize_title(normalized) == normalized


def test_counts_and_percentages_keep_all_source_records():
    item = get_proceeding("acl", "2025mainlong")
    point = analyze_titles(item, ["knowledge", "other topic", "knowledge"], ["knowledge"])
    assert (point.count, point.total, point.ratio) == (2, 3, 2 / 3 * 100)
    assert [match.paper.source_index for match in point.matches] == [1, 3]
    assert math.isnan(analyze_titles(item, [], ["knowledge"]).ratio)


@pytest.mark.parametrize(
    "title, keywords, delta, reason",
    [
        ("Graph-based learning", ["graph"], 1, "title_normalization"),
        ("Chemical reagents", ["agent"], -1, "title_normalization"),
        ("Knowledge graphs", ["knowledge graphs"], 1, "query_normalization_or_phrase"),
        ("LLM models", ["LLM"], 1, "query_normalization_or_phrase"),
    ],
)
def test_comparison_explains_each_changed_paper(title, keywords, delta, reason):
    item = get_proceeding("acl", "2025mainlong")
    summary, changes = compare_papers(item, [paper_from_title(title, 1, item.parser)], keywords)
    assert summary["delta"] == delta
    assert summary["added"] - summary["removed"] == delta
    assert len(changes) == 1
    assert changes[0]["original_title"] == title
    assert changes[0]["reason"] == reason
