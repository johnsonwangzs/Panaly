"""Pure keyword matching and counting; no filesystem or plotting dependencies."""

import re
from collections.abc import Sequence

from panaly.models import Proceeding, TrendPoint


def find_matches(titles: Sequence[str], keywords: Sequence[str]) -> list[str]:
    """Match any keyword against complete tokens, preserving the original rules.

    Callers supply lowercase keywords. Punctuation is deleted before splitting;
    multiword phrases and substring matches remain outside phase-one scope.
    """
    matches = []
    for title in titles:
        tokens = re.sub(r"[^\w\s]", "", title.lower()).split()
        if any(keyword == token for token in tokens for keyword in keywords):
            matches.append(title)
    return matches


def analyze_titles(
    proceeding: Proceeding, titles: Sequence[str], keywords: Sequence[str]
) -> TrendPoint:
    return TrendPoint(proceeding, count=len(find_matches(titles, keywords)), total=len(titles))
