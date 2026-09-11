"""Thin adapters for the original top-level Python imports.

New code should use config, pipeline, analysis, and plotting directly. Path maps
on Config are compatibility snapshots; edit the catalogue instead of those maps.
"""

from pathlib import Path

from panaly.analysis import analyze_papers
from panaly.config import PROCEEDINGS, get_proceeding
from panaly.download import download_source
from panaly.models import TrendPoint
from panaly.parsers import parse_titles
from panaly.paths import Paths
from panaly.pipeline import extract_titles, read_papers, read_titles, run_trend, run_wordcloud
from panaly.plotting import plot_trend
from panaly.plotting import plot_wordcloud as render_wordcloud
from panaly.terminology import STOP_WORDS, TERMINOLOGY


class Config:
    support_conference = list(PROCEEDINGS)
    tidy_terminology = TERMINOLOGY
    stop_word = STOP_WORDS
    src_url = {
        conference: {key: item.url for key, item in entries.items()}
        for conference, entries in PROCEEDINGS.items()
    }
    src_file = {
        conference: {key: str(Paths().source_path(item)) for key, item in entries.items()}
        for conference, entries in PROCEEDINGS.items()
    }
    title_file = {
        conference: {key: str(Paths().readable_titles_path(item)) for key, item in entries.items()}
        for conference, entries in PROCEEDINGS.items()
    }
    # Only these two proceedings were configured for the experimental LLM script.
    keyword_file = {
        "acl": {
            "2024mainlong": "resources/keyword_acl24mainlong.txt",
            "2024findlong": "resources/keyword_acl24findlong.txt",
        }
    }


def dl_resource(conf_proceedings):
    for conference, keys in conf_proceedings.items():
        for key in keys:
            download_source(get_proceeding(conference, key), Paths())


class Downloader:
    def __init__(self, dl_target):
        self.dl_target = dl_target

    def download_files(self):
        dl_resource(self.dl_target)


def extract_title(conf_proceedings):
    for conference, keys in conf_proceedings.items():
        for key in keys:
            extract_titles(get_proceeding(conference, key), Paths())


class TitleExtractor:
    def __init__(self, conference, proceeding):
        self.conference = conference
        self.proceeding = proceeding

    def extract_title_from_html_nips(self, file_path):
        return parse_titles(Path(file_path).read_text(encoding="utf-8"), "nips_html")

    def extract_title_from_html_aclweb(self, file_path):
        return parse_titles(Path(file_path).read_text(encoding="utf-8"), "acl_html")

    def extract_title_from_html_iclr(self, file_path):
        return parse_titles(Path(file_path).read_text(encoding="utf-8"), "downloads_html")

    def extract_title_from_bib(self, file_path):
        return parse_titles(Path(file_path).read_text(encoding="utf-8"), "bibtex")


class PaperSearcher:
    def __init__(self, conf_proceedings, keywords):
        self.conf_proceedings = conf_proceedings
        self.keywords = keywords

    def search(self):
        record = {}
        for conference, keys in self.conf_proceedings.items():
            if conference not in PROCEEDINGS:
                continue
            record[conference] = {}
            for key in keys:
                if key not in PROCEEDINGS[conference]:
                    continue
                item = get_proceeding(conference, key)
                result = analyze_papers(item, read_papers(item, Paths()), self.keywords)
                for match in result.matches:
                    print(f"{conference}-{key} | {match.paper.original_title.strip()}")
                record[conference][key] = result.count
        return sum(sum(counts.values()) for counts in record.values()), record


def search_paper(conf_proceedings, keywords):
    total, record = PaperSearcher(conf_proceedings, keywords).search()
    print(f"检索完成，共找到 {total} 篇含关键字的论文。")
    print(record)
    return record


class TendAnalyzer:
    def __init__(self, conf_proceedings, keywords):
        self.conf_proceedings = conf_proceedings
        self.keywords = keywords

    def draw_plot(self, description, record, *, show=False):
        targets = []
        for conference, counts in record.items():
            points = []
            for key, count in reversed(list(counts.items())):
                item = get_proceeding(conference, key)
                points.append(TrendPoint(item, count, len(read_titles(item, Paths()))))
            targets.append(plot_trend(points, description, show=show))
        return targets


def analyze_tendency(conf_proceedings, description, keywords, *, show=False):
    record = search_paper(conf_proceedings, keywords)
    return TendAnalyzer(conf_proceedings, keywords).draw_plot(description, record, show=show)


def gen_wordcloud(conference, proceeding, max_words, *, show=False):
    item = get_proceeding(conference, proceeding)
    return render_wordcloud(item, read_titles(item, Paths()), max_words, show=show)


def plot_wordcloud(max_words=150, conference="acl", proceeding="2025mainlong", *, show=False):
    return run_wordcloud(get_proceeding(conference, proceeding), max_words, show=show)


def plot_tendency(conf_proceedings, description, keywords, *, show=False):
    return [
        run_trend(
            [get_proceeding(conference, key) for key in reversed(keys)],
            keywords,
            description,
            show=show,
        )
        for conference, keys in conf_proceedings.items()
    ]
