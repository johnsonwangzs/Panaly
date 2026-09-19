import subprocess
import sys
from pathlib import Path

import pytest

from experiments import extract_keyword as experiment
from panaly.config import get_proceeding
from panaly.paths import Paths


@pytest.mark.parametrize("legacy", [False, True])
def test_keyword_experiment_reuses_titles_and_preserves_output(tmp_path, monkeypatch, legacy):
    paths = Paths(tmp_path / "data", tmp_path / "outputs", tmp_path / "resources")
    item = get_proceeding("acl", "2024mainlong")
    source = paths.legacy_dir / "title_acl24mainlong.txt" if legacy else paths.titles_path(item)
    source.parent.mkdir(parents=True)
    source.write_text("LLM for knowledge\n", encoding="utf-8")

    class FakeExtractor:
        def __init__(self, model):
            assert model == "kimi"

        def extract_keyword_kimi(self, titles):
            assert titles == ["LLM for knowledge\n"]
            return ["LLM, knowledge"]

    monkeypatch.setattr(experiment, "KeywordExtractor", FakeExtractor)
    target = experiment.extract_keyword("acl", "2024mainlong", paths=paths)
    assert target == paths.legacy_dir / "keyword_acl24mainlong.txt"
    assert target.read_text(encoding="utf-8") == "LLM, knowledge\n"
    assert source.read_text(encoding="utf-8") == "LLM for knowledge\n"


def test_keyword_experiment_requires_explicit_credentials(monkeypatch):
    monkeypatch.delenv("MOONSHOT_API_KEY", raising=False)
    with pytest.raises(ValueError, match="MOONSHOT_API_KEY"):
        experiment.KeywordExtractor()


@pytest.mark.parametrize("entry", [["-m", "experiments.extract_keyword"], ["extract_keyword.py"]])
def test_experiment_help_does_not_require_optional_sdk(entry):
    result = subprocess.run(
        [sys.executable, "-S", *entry, "--help"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    assert "python -m experiments.extract_keyword" in result.stdout
