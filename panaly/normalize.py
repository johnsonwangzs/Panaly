"""Boundary-aware, one-pass terminology normalization shared by titles and queries."""

import re
import unicodedata
from functools import lru_cache

from panaly.terminology import TERMINOLOGY

NORMALIZATION_VERSION = 2
Definitions = tuple[tuple[str, tuple[str, ...]], ...]


def tokenize(text: str) -> tuple[str, ...]:
    """Treat punctuation, Unicode hyphens, and underscores as word separators."""
    return tuple(re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", text).casefold()))


@lru_cache(maxsize=8)
def _compile_aliases(definitions: Definitions) -> tuple[dict[str, str], re.Pattern[str]]:
    aliases = {}
    for canonical, variants in definitions:
        for variant in (canonical, *variants):
            phrase = " ".join(tokenize(variant))
            if phrase:
                aliases.setdefault(phrase, canonical)
    # A longer phrase wins before a nested one, e.g. large language model before LM.
    phrases = sorted(aliases, key=lambda phrase: (-len(phrase.split()), -len(phrase)))
    expression = "|".join(re.escape(phrase) for phrase in phrases) or r"(?!)"
    return aliases, re.compile(r"(?<!\w)(?:" + expression + r")(?!\w)")


def _definitions() -> Definitions:
    # Include configuration in the cache key, so interactive edits take effect too.
    return tuple((term, tuple(variants)) for term, variants in TERMINOLOGY.items())


def prepare_terminology() -> dict[str, re.Pattern[str]]:
    """Compatibility helper: patterns operate on space-separated lowercase tokens."""
    patterns = {}
    for term, variants in _definitions():
        _, pattern = _compile_aliases(((term, variants),))
        patterns[term] = pattern
    return patterns


def normalize_title(text: str) -> str:
    aliases, pattern = _compile_aliases(_definitions())
    tokens = " ".join(tokenize(text))
    return pattern.sub(lambda match: aliases[match.group()], tokens)


def substitute_terminology(text: str) -> str:
    return normalize_title(text)
