"""Render already prepared data; rendering never downloads or parses papers."""

from collections.abc import Sequence
from contextlib import contextmanager
from pathlib import Path

from panaly.models import Proceeding, TrendPoint
from panaly.paths import safe_description
from panaly.terminology import STOP_WORDS


@contextmanager
def _figure(show: bool, **kwargs):
    if show:
        import matplotlib.pyplot as plt

        figure = plt.figure(**kwargs)
    else:
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from matplotlib.figure import Figure

        # Saving a plot must not switch the caller's backend or close their windows.
        figure = Figure(**kwargs)
        FigureCanvasAgg(figure)
    try:
        yield figure
        if show:
            plt.show()
    finally:
        if show:
            plt.close(figure)
        else:
            figure.clear()


def plot_trend(
    points: Sequence[TrendPoint],
    description: str,
    output_dir: Path = Path("outputs"),
    *,
    show: bool = False,
) -> Path:
    conference = points[0].proceeding.conference
    labels = [point.proceeding.key for point in points]
    with _figure(show) as fig:
        ax1 = fig.subplots()
        ax1.plot(labels, [point.ratio for point in points], color="g", marker="o", label="占比")
        ax2 = ax1.twinx()
        ax2.bar(labels, [point.count for point in points], color="r", alpha=0.4, label="数量")
        ax1.set_title(
            f"Ratio & Number for [{description}]-related \n"
            f"Papers in [{conference.upper()}] Proceedings"
        )
        ax1.set_xlabel("Proceeding")
        ax1.set_ylabel("Keywords-related Paper / Total (%)")
        ax2.set_ylabel("Number")
        ax1.tick_params(axis="x", rotation=45, labelsize="small")
        ax2.grid(True)
        fig.tight_layout()
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = safe_description(description)
        target = output_dir / f"plot_{conference}_{filename}.png"
        fig.savefig(target)
        return target


def create_wordcloud(titles: Sequence[str], max_words: int = 150):
    from wordcloud import STOPWORDS, WordCloud

    # Preserve the exact text stream previously read from the title file.
    text = "".join(", " + title.removesuffix("\n") + "\n" for title in titles)
    return WordCloud(
        width=1600,
        height=800,
        background_color="white",
        max_words=max_words,
        stopwords=STOPWORDS.union(set(STOP_WORDS)),
    ).generate(text)


def plot_wordcloud(
    proceeding: Proceeding,
    titles: Sequence[str],
    max_words: int = 150,
    output_dir: Path = Path("outputs"),
    *,
    show: bool = False,
) -> Path:
    wordcloud = create_wordcloud(titles, max_words)
    with _figure(show, figsize=(20, 10), dpi=500) as fig:
        axes = fig.subplots()
        axes.imshow(wordcloud, interpolation="bilinear")
        axes.axis("off")
        output_dir.mkdir(parents=True, exist_ok=True)
        target = output_dir / (
            f"wordcloud_{proceeding.conference}{proceeding.key}_top{max_words}.png"
        )
        fig.savefig(target, dpi=500)
        return target
