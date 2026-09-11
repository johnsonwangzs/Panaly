"""Command-line interface for catalogue inspection, trends, and wordclouds."""

import argparse
import logging
from pathlib import Path

from panaly.config import PROCEEDINGS, select_proceedings
from panaly.paths import Paths


def _positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("请输入正整数。")
    return number


def _add_paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--data-dir", type=Path, default=Path("data"), help="原始和处理后数据目录")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="图表输出目录")
    parser.add_argument("--legacy-dir", type=Path, default=Path("resources"), help="旧版缓存目录")
    parser.add_argument("--show", action="store_true", help="保存后打开图形窗口")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="panaly", description="分析学术会议论文标题中的热点和趋势。"
    )
    commands = parser.add_subparsers(dest="command")

    listing = commands.add_parser("list", help="查看已配置的会议和论文集")
    listing.add_argument("--conference", choices=PROCEEDINGS)

    trend = commands.add_parser("trend", help="统计关键词相关论文数量与占比，并绘制趋势图")
    trend.add_argument("--conference", required=True, choices=PROCEEDINGS)
    selection = trend.add_mutually_exclusive_group(required=True)
    selection.add_argument("--years", nargs="+", type=int, help="年份；默认选择各年的主会分卷")
    selection.add_argument("--proceedings", nargs="+", help="完整论文集 ID，例如 2025mainlong")
    trend.add_argument("--track", help="年份对应的分卷后缀，例如 findlong、benchmark")
    trend.add_argument("--keywords", required=True, nargs="+", help="小写关键词；匹配其中任意一个")
    trend.add_argument("--description", help="图表主题描述，默认使用关键词")
    _add_paths(trend)

    wordcloud = commands.add_parser("wordcloud", help="生成单个论文集的标题词云")
    wordcloud.add_argument("--conference", required=True, choices=PROCEEDINGS)
    selection = wordcloud.add_mutually_exclusive_group(required=True)
    selection.add_argument("--year", type=int, help="年份；默认选择主会分卷")
    selection.add_argument("--proceeding", help="完整论文集 ID")
    wordcloud.add_argument("--track", help="年份对应的分卷后缀")
    wordcloud.add_argument("--max-words", type=_positive_int, default=150)
    _add_paths(wordcloud)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "list":
        conferences = [args.conference] if args.conference else PROCEEDINGS
        for conference in conferences:
            print(f"{conference}: {' '.join(PROCEEDINGS[conference])}")
        return 0

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    paths = Paths(args.data_dir, args.output_dir, args.legacy_dir)
    try:
        if args.command == "trend":
            proceedings = select_proceedings(
                args.conference, years=args.years, keys=args.proceedings, track=args.track
            )
            from panaly.pipeline import run_trend

            points, target = run_trend(
                proceedings,
                args.keywords,
                args.description or "_".join(args.keywords),
                paths,
                show=args.show,
            )
            print("论文集\t相关论文\t论文总数\t占比 (%)")
            for point in points:
                print(f"{point.proceeding.key}\t{point.count}\t{point.total}\t{point.ratio:.6f}")
        else:
            proceedings = select_proceedings(
                args.conference,
                years=[args.year] if args.year is not None else None,
                keys=[args.proceeding] if args.proceeding is not None else None,
                track=args.track,
            )
            from panaly.pipeline import run_wordcloud

            target = run_wordcloud(proceedings[0], args.max_words, paths, show=args.show)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"图表保存至: {target.resolve()}")
    return 0
