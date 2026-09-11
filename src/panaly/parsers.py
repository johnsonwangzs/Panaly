"""Parse source content without downloading, writing files, or plotting."""

import re

import bibtexparser
from bs4 import BeautifulSoup

from panaly.models import Parser
from panaly.normalize import normalize_title


def parse_titles(content: str, parser: Parser) -> list[str]:
    if parser == "bibtex":
        return [
            normalize_title(re.sub(r"{(.*?)}", r"\1", entry.get("title")))
            for entry in bibtexparser.loads(content).entries
        ]

    selectors = {
        "acl_html": ("section.page__content ul", "strong"),
        "downloads_html": ("div.list_html ul", "a"),
        "nips_html": ("div.container-fluid ul", "a"),
    }
    selector, title_tag = selectors[parser]
    lists = BeautifulSoup(content, "html.parser").select(selector)
    if not lists:
        return []
    # The old ACL parser selects the second list, falling back to the first.
    selected = lists[1] if parser == "acl_html" and len(lists) > 1 else lists[0]
    titles = []
    for item in selected.find_all("li"):
        tag = item.find(title_tag)
        if tag:
            titles.append(normalize_title(tag.text))
    return titles
