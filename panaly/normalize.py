"""The original ordered replacement rules, intentionally unchanged in phase one."""

import re

from panaly.terminology import TERMINOLOGY


def prepare_terminology() -> dict[str, re.Pattern[str]]:
    return {
        term: re.compile("|".join(re.escape(v.lower()) for v in variants), re.IGNORECASE)
        for term, variants in TERMINOLOGY.items()
    }


def substitute_terminology(text: str) -> str:
    for term, pattern in prepare_terminology().items():
        text = pattern.sub(" " + term + " ", text)
    return text


def normalize_title(text: str) -> str:
    return substitute_terminology(re.sub(r"\s+", " ", text).lower())
