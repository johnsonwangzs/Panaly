import subprocess
import sys
from pathlib import Path

import pytest

from panaly.cli import main
from panaly.config import get_proceeding, select_proceedings
from panaly.download import download_source
from panaly.paths import Paths, legacy_source_name


@pytest.mark.parametrize("entry", [["main.py"], ["-m", "panaly"]])
def test_entry_points_run_from_source_without_site_packages(entry):
    result = subprocess.run(
        [sys.executable, "-S", *entry, "list", "--conference", "acl"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    assert "2025mainlong" in result.stdout


def test_year_selection_defaults_to_main_and_orders_chronologically():
    selected = select_proceedings("acl", years=[2025, 2022, 2025])
    assert [item.key for item in selected] == ["2022mainlong", "2025mainlong"]
    assert select_proceedings("acl", years=[2025], track="findlong")[0].key == "2025findlong"
    assert select_proceedings("acl", years=[2020])[0].key == "2020main"
    assert select_proceedings("nips", years=[2022])[0].key == "2022main&benchmark"
    assert select_proceedings("nips", keys=["2021benchmark"])[0].key == "2021benchmark"


@pytest.mark.parametrize(
    "arguments",
    [
        ["trend", "--conference", "acl", "--years", "2099", "--keywords", "knowledge"],
        ["wordcloud", "--conference", "acl", "--year", "2025", "--max-words", "0"],
        ["wordcloud", "--conference", "acl", "--proceeding", "missing"],
        ["wordcloud", "--conference", "acl", "--proceeding", "2025mainlong", "--track", "mainlong"],
        ["trend", "--conference", "acl", "--years", "2025", "--keywords", "???"],
    ],
)
def test_invalid_cli_selection_fails_before_data_access(arguments, capsys):
    with pytest.raises(SystemExit) as error:
        main(arguments)
    assert error.value.code == 2
    assert "error:" in capsys.readouterr().err


def test_list_command(capsys):
    assert main(["list", "--conference", "acl"]) == 0
    output = capsys.readouterr().out
    assert "2025mainlong" in output
    assert "icml" not in output


def test_trend_command_reuses_cache_without_modifying_it(tmp_path, monkeypatch, capsys):
    def no_network(*args, **kwargs):
        pytest.fail("The cached source must not be downloaded again")

    monkeypatch.setattr("panaly.download.urlretrieve", no_network)
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    item = get_proceeding("acl", "2025mainlong")
    source = legacy / legacy_source_name(item)
    original = (Path(__file__).parent / "fixtures/acl.html").read_bytes()
    source.write_bytes(original)
    data, output = tmp_path / "data", tmp_path / "plots"
    assert (
        main(
            [
                "trend",
                "--conference",
                "acl",
                "--years",
                "2025",
                "--keywords",
                "knowledge",
                "--legacy-dir",
                str(legacy),
                "--data-dir",
                str(data),
                "--output-dir",
                str(output),
            ]
        )
        == 0
    )
    assert "2025mainlong\t1\t3\t33.333333" in capsys.readouterr().out
    assert source.read_bytes() == original
    assert (data / "processed/acl/2025mainlong.txt").exists()
    assert (output / "plot_acl_knowledge.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert not (data / "raw").exists()


def test_new_download_goes_to_generated_raw_path(tmp_path, monkeypatch):
    paths = Paths(tmp_path / "data", tmp_path / "output", tmp_path / "legacy")
    item = get_proceeding("icml", "2025")
    calls = []

    def fake_download(url, target):
        calls.append(url)
        target.write_text("cached source", encoding="utf-8")

    monkeypatch.setattr("panaly.download.urlretrieve", fake_download)
    assert download_source(item, paths) == paths.raw_path(item)
    assert download_source(item, paths) == paths.raw_path(item)
    assert calls == [item.url]
