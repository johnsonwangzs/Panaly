"""Single source of truth for the 89 configured proceedings."""

from collections.abc import Sequence

from panaly.models import Parser, Proceeding


def _entries(conference: str, parser: Parser, sources: dict[str, str]) -> dict[str, Proceeding]:
    return {key: Proceeding(conference, key, url, parser) for key, url in sources.items()}


PROCEEDINGS: dict[str, dict[str, Proceeding]] = {
    "acl": {
        **_entries(
            "acl",
            "acl_html",
            {
                "2025mainlong": "https://2025.aclweb.org/program/main_papers/",
                "2025findlong": "https://2025.aclweb.org/program/find_papers/",
            },
        ),
        **_entries(
            "acl",
            "bibtex",
            {
                "2024mainlong": "https://aclanthology.org/volumes/2024.acl-long.bib",
                "2024findlong": "https://aclanthology.org/volumes/2024.findings-acl.bib",
                "2023mainlong": "https://aclanthology.org/volumes/2023.acl-long.bib",
                "2023findlong": "https://aclanthology.org/volumes/2023.findings-acl.bib",
                "2022mainlong": "https://aclanthology.org/volumes/2022.acl-long.bib",
                "2022findlong": "https://aclanthology.org/volumes/2022.findings-acl.bib",
                "2021mainlong": "https://aclanthology.org/volumes/2021.acl-long.bib",
                "2021findlong": "https://aclanthology.org/volumes/2021.findings-acl.bib",
                "2020main": "https://aclanthology.org/volumes/2020.acl-main.bib",
                "2019main": "https://aclanthology.org/volumes/P19-1.bib",
                "2018main": "https://aclanthology.org/volumes/P18-1.bib",
                "2017main": "https://aclanthology.org/volumes/P17-1.bib",
                "2016main": "https://aclanthology.org/volumes/P16-1.bib",
                "2015main": "https://aclanthology.org/volumes/P15-1.bib",
                "2014main": "https://aclanthology.org/volumes/P14-1.bib",
                "2013main": "https://aclanthology.org/volumes/P13-1.bib",
                "2012main": "https://aclanthology.org/volumes/P12-1.bib",
                "2011main": "https://aclanthology.org/volumes/P11-1.bib",
                "2010main": "https://aclanthology.org/volumes/P10-1.bib",
            },
        ),
    },
    "coling": {
        **_entries(
            "coling",
            "bibtex",
            {
                "2025main": "https://aclanthology.org/volumes/2025.coling-main.bib",
                "2024main": "https://aclanthology.org/volumes/2024.lrec-main.bib",
                "2022main": "https://aclanthology.org/volumes/2022.coling-1.bib",
                "2020main": "https://aclanthology.org/volumes/2020.coling-main.bib",
                "2018main": "https://aclanthology.org/volumes/C18-1.bib",
                "2016main": "https://aclanthology.org/volumes/C16-1.bib",
                "2014main": "https://aclanthology.org/volumes/C14-1.bib",
                "2012main": "https://aclanthology.org/volumes/C12-1.bib",
                "2010main": "https://aclanthology.org/volumes/C10-1.bib",
            },
        ),
    },
    "emnlp": {
        **_entries(
            "emnlp",
            "bibtex",
            {
                "2024main": "https://aclanthology.org/volumes/2024.emnlp-main.bib",
                "2023main": "https://aclanthology.org/volumes/2023.emnlp-main.bib",
                "2022main": "https://aclanthology.org/volumes/2022.emnlp-main.bib",
                "2021main": "https://aclanthology.org/volumes/2021.emnlp-main.bib",
                "2020main": "https://aclanthology.org/volumes/D20-1.bib",
                "2019main": "https://aclanthology.org/volumes/D19-1.bib",
                "2018main": "https://aclanthology.org/volumes/D18-1.bib",
                "2017main": "https://aclanthology.org/volumes/D17-1.bib",
                "2016main": "https://aclanthology.org/volumes/D16-1.bib",
                "2015main": "https://aclanthology.org/volumes/D15-1.bib",
                "2014main": "https://aclanthology.org/volumes/D14-1.bib",
                "2013main": "https://aclanthology.org/volumes/D13-1.bib",
                "2012main": "https://aclanthology.org/volumes/D12-1.bib",
                "2011main": "https://aclanthology.org/volumes/D11-1.bib",
                "2010main": "https://aclanthology.org/volumes/D10-1.bib",
            },
        ),
    },
    "iclr": {
        **_entries(
            "iclr",
            "downloads_html",
            {
                "2025": "https://iclr.cc/Downloads/2025",
                "2024": "https://iclr.cc/Downloads/2024",
                "2023": "https://iclr.cc/Downloads/2023",
                "2022": "https://iclr.cc/Downloads/2022",
                "2021": "https://iclr.cc/Downloads/2021",
                "2020": "https://iclr.cc/Downloads/2020",
                "2019": "https://iclr.cc/Downloads/2019",
                "2018": "https://iclr.cc/Downloads/2018",
            },
        ),
    },
    "icml": {
        **_entries(
            "icml",
            "downloads_html",
            {
                "2025": "https://icml.cc/Downloads/2025",
                "2024": "https://icml.cc/Downloads/2024",
                "2023": "https://icml.cc/Downloads/2023",
                "2022": "https://icml.cc/Downloads/2022",
                "2021": "https://icml.cc/Downloads/2021",
                "2020": "https://icml.cc/Downloads/2020",
                "2019": "https://icml.cc/Downloads/2019",
                "2018": "https://icml.cc/Downloads/2018",
                "2017": "https://icml.cc/Downloads/2017",
            },
        ),
    },
    "naacl": {
        **_entries(
            "naacl",
            "bibtex",
            {
                "2025mainlong": "https://aclanthology.org/volumes/2025.naacl-long.bib",
                "2024mainlong": "https://aclanthology.org/volumes/2024.naacl-long.bib",
                "2022mainlong": "https://aclanthology.org/volumes/2022.naacl-main.bib",
                "2021mainlong": "https://aclanthology.org/volumes/2021.naacl-main.bib",
                "2019mainlong": "https://aclanthology.org/volumes/N19-1.bib",
                "2018mainlong": "https://aclanthology.org/volumes/N18-1.bib",
                "2016main": "https://aclanthology.org/volumes/N16-1.bib",
                "2015main": "https://aclanthology.org/volumes/N15-1.bib",
                "2013main": "https://aclanthology.org/volumes/N13-1.bib",
                "2012main": "https://aclanthology.org/volumes/N12-1.bib",
                "2010main": "https://aclanthology.org/volumes/N10-1.bib",
            },
        ),
    },
    "nips": {
        **_entries(
            "nips",
            "nips_html",
            {
                "2024main&benchmark": "https://papers.nips.cc/paper_files/paper/2024",
                "2023main&benchmark": "https://papers.nips.cc/paper_files/paper/2023",
                "2022main&benchmark": "https://papers.nips.cc/paper_files/paper/2022",
                "2021main": "https://papers.nips.cc/paper_files/paper/2021",
                "2021benchmark": "https://datasets-benchmarks-proceedings.neurips.cc/paper/2021",
                "2020": "https://papers.nips.cc/paper_files/paper/2020",
                "2019": "https://papers.nips.cc/paper_files/paper/2019",
                "2018": "https://papers.nips.cc/paper_files/paper/2018",
                "2017": "https://papers.nips.cc/paper_files/paper/2017",
                "2016": "https://papers.nips.cc/paper_files/paper/2016",
                "2015": "https://papers.nips.cc/paper_files/paper/2015",
                "2014": "https://papers.nips.cc/paper_files/paper/2014",
                "2013": "https://papers.nips.cc/paper_files/paper/2013",
                "2012": "https://papers.nips.cc/paper_files/paper/2012",
                "2011": "https://papers.nips.cc/paper_files/paper/2011",
                "2010": "https://papers.nips.cc/paper_files/paper/2010",
            },
        ),
    },
}


def get_proceeding(conference: str, key: str) -> Proceeding:
    try:
        return PROCEEDINGS[conference][key]
    except KeyError:
        raise ValueError(f"未配置论文集: {conference}/{key}；请用 list 命令查看。") from None


def select_proceedings(
    conference: str,
    *,
    years: Sequence[int] | None = None,
    keys: Sequence[str] | None = None,
    track: str | None = None,
) -> list[Proceeding]:
    """Resolve CLI selections, using the main volume by default for each year."""
    if conference not in PROCEEDINGS:
        raise ValueError(f"未配置会议: {conference}")
    if (years is None) == (keys is None):
        raise ValueError("请选择年份或论文集 ID。")
    if keys is not None:
        if track is not None:
            raise ValueError("--track 只能与年份参数一起使用。")
        selected = [get_proceeding(conference, key) for key in dict.fromkeys(keys)]
    else:
        selected = []
        for year in dict.fromkeys(years):
            candidates = [item for item in PROCEEDINGS[conference].values() if item.year == year]
            tracks = (track,) if track is not None else ("mainlong", "main", "", "main&benchmark")
            match = next(
                (item for preferred in tracks for item in candidates if item.track == preferred),
                None,
            )
            if match is None:
                raise ValueError(
                    f"未配置 {conference}/{year} 的指定分卷；请用 list 查看完整论文集 ID。"
                )
            selected.append(match)
    return sorted(selected, key=lambda item: (item.year, item.key))
