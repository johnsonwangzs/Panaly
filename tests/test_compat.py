from pathlib import Path

from main import plot_tendency
from search_paper import PaperSearcher


def test_original_imports_work_with_existing_cache(tmp_path, monkeypatch):
    fixture = (Path(__file__).parent / "fixtures/acl.html").read_bytes()
    monkeypatch.chdir(tmp_path)
    legacy = tmp_path / "resources"
    legacy.mkdir()
    (legacy / "2025.acl.main.html").write_bytes(fixture)
    selection = {"acl": ["2025mainlong"]}

    results = plot_tendency(selection, "knowledge", ["knowledge"])
    points, target = results[0]
    assert points[0].count == 1
    assert points[0].total == 3
    assert target == Path("outputs/plot_acl_knowledge.png")
    assert target.exists()
    assert PaperSearcher(selection, ["knowledge"]).search() == (1, {"acl": {"2025mainlong": 1}})
