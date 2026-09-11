import math

from panaly.analysis import analyze_titles, find_matches
from panaly.config import get_proceeding
from panaly.normalize import normalize_title


def test_matching_preserves_token_rules_and_counts_a_paper_once():
    titles = ["Agent agent and LM", "agents", "multi-agent", "LLM/LM", "LLM for reasoning"]
    assert find_matches(titles, ["agent", "llm", "lm", "agent"]) == [titles[0], titles[4]]
    assert find_matches(["language model"], ["language model"]) == []
    assert find_matches(["LLM"], ["LLM"]) == []  # Legacy callers must use lowercase keywords.


def test_terminology_replacements_keep_order_and_spacing():
    assert normalize_title("Large Language Models and language models") == " LLM  and  LM "


def test_counts_and_percentages():
    item = get_proceeding("acl", "2025mainlong")
    point = analyze_titles(item, ["knowledge", "other topic", "knowledge knowledge"], ["knowledge"])
    assert (point.count, point.total, point.ratio) == (2, 3, 2 / 3 * 100)
    assert math.isnan(analyze_titles(item, [], ["knowledge"]).ratio)
