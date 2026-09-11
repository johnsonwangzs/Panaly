import matplotlib
import matplotlib.pyplot as plt

from panaly.config import get_proceeding
from panaly.models import TrendPoint
from panaly.plotting import plot_trend


def test_saving_does_not_change_backend_or_close_existing_figures(tmp_path):
    backend = matplotlib.get_backend()
    existing = plt.figure()
    point = TrendPoint(get_proceeding("acl", "2025mainlong"), 1, 3)
    try:
        plot_trend([point], "knowledge", tmp_path)
        assert matplotlib.get_backend() == backend
        assert plt.fignum_exists(existing.number)
    finally:
        plt.close(existing)


def test_show_is_explicit_and_closes_its_own_figure(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(plt, "show", lambda: calls.append(plt.gcf().number))
    point = TrendPoint(get_proceeding("acl", "2025mainlong"), 1, 3)
    target = plot_trend([point], "knowledge", tmp_path, show=True)
    assert target.exists()
    assert len(calls) == 1
    assert not plt.fignum_exists(calls[0])
