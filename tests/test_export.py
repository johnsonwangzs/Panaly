import csv
import hashlib
import json
from pathlib import Path

import pytest

from panaly.config import get_proceeding
from panaly.normalize import normalize_title
from panaly.paths import Paths, report_paths
from panaly.pipeline import extract_papers, read_papers, run_trend


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def test_json_preserves_originals_and_refreshes_normalization(tmp_path):
    paths = Paths(tmp_path / "data", tmp_path / "outputs", tmp_path / "legacy")
    item = get_proceeding("acl", "2025mainlong")
    source = paths.raw_path(item)
    source.parent.mkdir(parents=True)
    raw = '<section class="page__content"><ul><li><strong>Large Language Models</strong></li></ul></section>'
    source.write_text(raw, encoding="utf-8")
    papers = extract_papers(item, paths)
    assert papers[0].original_title == "Large Language Models"
    assert papers[0].normalized_title == "LLM"
    document = json.loads(paths.papers_path(item).read_text(encoding="utf-8"))
    assert document["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert document["normalization_version"] == 2
    assert document["papers"][0]["original_title"] == "Large Language Models"
    # A stored standardized title must never be mistaken for the source title.
    document["papers"][0]["normalized_title"] = "obsolete cached text"
    paths.papers_path(item).write_text(json.dumps(document), encoding="utf-8")
    source.unlink()
    assert read_papers(item, paths)[0] == papers[0]


def test_normalized_text_alone_cannot_be_presented_as_original(tmp_path):
    paths = Paths(tmp_path / "data", tmp_path / "outputs", tmp_path / "legacy")
    item = get_proceeding("acl", "2025mainlong")
    paths.titles_path(item).parent.mkdir(parents=True)
    paths.titles_path(item).write_text("LLM title\n", encoding="utf-8")
    with pytest.raises(FileNotFoundError, match="旧版 txt"):
        read_papers(item, paths)


@pytest.mark.parametrize("keywords, count", [(["LLM", "knowledge"], 1), (["no such phrase"], 0)])
def test_trend_exports_reconcile_with_papers_and_preserve_csv_text(tmp_path, keywords, count):
    paths = Paths(tmp_path / "data", tmp_path / "outputs", tmp_path / "legacy")
    item = get_proceeding("acl", "2025mainlong")
    source = paths.raw_path(item)
    source.parent.mkdir(parents=True)
    original = 'LLM, "Knowledge"\nwith Graphs'
    source.write_text(
        '<section class="page__content"><ul><li><strong>'
        + original
        + "</strong></li><li><strong>Other</strong></li></ul></section>",
        encoding="utf-8",
        newline="",
    )
    points, image = run_trend([item], keywords, "a/b:topic", paths, compare_legacy=True)
    targets = report_paths("acl", "a/b:topic", paths.output_dir)
    summary = read_csv(targets["summary"])
    matches = read_csv(targets["papers"])
    assert image.exists()
    assert int(summary[0]["count"]) == points[0].count == len(matches) == count
    assert int(summary[0]["total"]) == 2
    assert float(summary[0]["ratio_percent"]) == count / 2 * 100
    assert targets["papers"].read_bytes().startswith(b"\xef\xbb\xbf")
    if count:
        assert matches[0]["original_title"] == original
        assert matches[0]["normalized_title"] == normalize_title(original)
        assert json.loads(matches[0]["matched_keywords"]) == keywords
        assert matches[0]["source_url"] == item.url
    metadata = json.loads(targets["metadata"].read_text(encoding="utf-8"))
    assert metadata["keywords"] == keywords
    assert metadata["comparison_enabled"] is True
    assert metadata["sources"][0]["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    comparison = read_csv(targets["comparison"])[0]
    changed = read_csv(targets["changes"])
    assert int(comparison["delta"]) == sum(1 if row["change"] == "added" else -1 for row in changed)
    assert all(path.parent == paths.output_dir for path in targets.values())


def test_legacy_searcher_uses_original_titles(tmp_path, monkeypatch, capsys):
    from search_paper import PaperSearcher

    fixture = (Path(__file__).parent / "fixtures/acl.html").read_bytes()
    monkeypatch.chdir(tmp_path)
    Path("resources").mkdir()
    Path("resources/2025.acl.main.html").write_bytes(fixture)
    total, _ = PaperSearcher({"acl": ["2025mainlong"]}, ["large language model"]).search()
    assert total == 1
    assert "Large Language Models for Knowledge" in capsys.readouterr().out
