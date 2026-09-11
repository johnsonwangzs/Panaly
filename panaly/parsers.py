"""Parse source content without downloading, writing files, or plotting."""

import re

from panaly.models import Paper, Parser
from panaly.normalize import normalize_title


def parse_original_titles(content: str, parser: Parser) -> list[str]:
    if parser == "bibtex":
        import bibtexparser

        return [entry["title"] for entry in bibtexparser.loads(content).entries]

    from bs4 import BeautifulSoup

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
            titles.append(tag.text)
    return titles


def paper_from_title(title: str, source_index: int, parser: Parser) -> Paper:
    # BibTeX case-protection braces are markup; keep them only in the original field.
    text = re.sub(r"{(.*?)}", r"\1", title) if parser == "bibtex" else title
    return Paper(source_index, title, normalize_title(text))


def parse_papers(content: str, parser: Parser) -> list[Paper]:
    return [
        paper_from_title(title, index, parser)
        for index, title in enumerate(parse_original_titles(content, parser), 1)
    ]


def parse_titles(content: str, parser: Parser) -> list[str]:
    """Compatibility API; use parse_papers when original titles are needed."""
    return [paper.normalized_title for paper in parse_papers(content, parser)]
