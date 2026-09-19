from pathlib import Path

import pytest


def test_original_imports_work_with_existing_cache(tmp_path, monkeypatch):
    # Only this compatibility test deliberately imports the deprecated root modules.
    with pytest.warns(DeprecationWarning, match="main.plot_tendency is deprecated"):
        from main import plot_tendency
    with pytest.warns(DeprecationWarning, match="search_paper is deprecated"):
        from search_paper import PaperSearcher

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
