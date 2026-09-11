"""Keyword and contiguous-phrase matching with per-paper evidence."""

from collections.abc import Sequence

from panaly.models import Paper, PaperMatch, Proceeding, TrendPoint
from panaly.normalize import normalize_title, tokenize


class KeywordMatcher:
    def __init__(self, keywords: Sequence[str]):
        self.queries: list[tuple[str, tuple[str, ...]]] = []
        seen = set()
        for keyword in keywords:
            phrase = tokenize(normalize_title(keyword))
            if not phrase:
                raise ValueError("关键词不能为空或只包含标点。")
            if phrase not in seen:
                self.queries.append((keyword.strip(), phrase))
                seen.add(phrase)
        if not self.queries:
            raise ValueError("至少需要一个关键词。")

    def match(self, normalized_title: str) -> tuple[str, ...]:
        tokens = tokenize(normalized_title)
        return tuple(
            label
            for label, phrase in self.queries
            if any(
                tokens[start : start + len(phrase)] == phrase
                for start in range(len(tokens) - len(phrase) + 1)
            )
        )


def find_matches(titles: Sequence[str], keywords: Sequence[str]) -> list[str]:
    matcher = KeywordMatcher(keywords)
    return [title for title in titles if matcher.match(normalize_title(title))]


def analyze_papers(
    proceeding: Proceeding, papers: Sequence[Paper], keywords: Sequence[str]
) -> TrendPoint:
    matcher = KeywordMatcher(keywords)
    matches = []
    for paper in papers:
        matched = matcher.match(paper.normalized_title)
        if matched:
            matches.append(PaperMatch(paper, matched))
    return TrendPoint(proceeding, len(matches), len(papers), tuple(matches))


def analyze_titles(
    proceeding: Proceeding, titles: Sequence[str], keywords: Sequence[str]
) -> TrendPoint:
    papers = [Paper(index, title, normalize_title(title)) for index, title in enumerate(titles, 1)]
    return analyze_papers(proceeding, papers, keywords)
