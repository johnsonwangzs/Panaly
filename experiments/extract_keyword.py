"""Optional LLM keyword extraction: python -m experiments.extract_keyword."""

import argparse
import os
from pathlib import Path

from panaly.config import PROCEEDINGS, get_proceeding
from panaly.paths import Paths, legacy_title_name


class KeywordExtractor:
    """Use the existing Moonshot experiment with credentials from the environment."""

    def __init__(self, model="kimi"):
        if model != "kimi":
            raise ValueError("当前实验仅支持 kimi。")
        self._init_kimi()
        # The optional SDK is not needed to import the module or display --help.
        from openai import OpenAI

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def _init_kimi(self):
        self.api_key = os.environ.get("MOONSHOT_API_KEY", "")
        if not self.api_key:
            raise ValueError("请通过 MOONSHOT_API_KEY 环境变量配置实验所需的 API Key。")
        self.base_url = os.environ.get("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1")
        self.model_name = os.environ.get("MOONSHOT_MODEL", "moonshot-v1-8k")

    def extract_keyword_kimi(self, titles: list[str]) -> list[str]:
        keywords = []
        for title in titles:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一个自然语言处理领域的专家。"},
                    {
                        "role": "user",
                        "content": f"列出这个论文题目中的英文关键词，将你的答案用逗号隔开：{title}",
                    },
                ],
                temperature=0.0,
            )
            keywords.append(completion.choices[0].message.content.strip())
            print(title.strip())
            print(keywords[-1])
        return keywords


def extract_keyword(conference: str, proceeding: str, *, paths: Paths = Paths()) -> Path:
    item = get_proceeding(conference, proceeding)
    with paths.readable_titles_path(item).open(encoding="utf-8") as stream:
        titles = stream.readlines()
    keywords = KeywordExtractor(model="kimi").extract_keyword_kimi(titles)
    # Preserve the original experiment's output names during the entry-point migration.
    target = paths.legacy_dir / legacy_title_name(item).replace("title_", "keyword_", 1)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(keyword + "\n" for keyword in keywords), encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m experiments.extract_keyword",
        description="使用 LLM 提取已缓存标题的关键词。",
    )
    parser.add_argument("--conference", choices=PROCEEDINGS, default="acl")
    parser.add_argument("--proceeding", default="2024mainlong")
    args = parser.parse_args(argv)
    try:
        target = extract_keyword(args.conference, args.proceeding)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"关键词保存至: {target.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
