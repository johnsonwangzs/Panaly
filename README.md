# Panaly

从学术会议论文标题中统计研究热点和年度趋势，支持下载论文列表、提取标题、术语归并、生成词云，以及绘制关键词相关论文的数量和占比。

目前配置了 ACL、COLING、EMNLP、ICLR、ICML、NAACL、NeurIPS（命令中使用 `nips`）共 89 个论文集，具体年份和分卷可通过 `list` 命令查看。

## 运行方式

使用现有的 Python 3.10 或以上环境，在项目根目录直接运行脚本。无需创建虚拟环境，也无需先将本项目安装成 Python 包。

脚本使用的第三方库列在 `requirements.txt`：Beautiful Soup、bibtexparser、Matplotlib 和 WordCloud。依赖沿用现有 Python 环境，项目不负责创建或切换环境。帮助和会议列表只使用 Python 标准库。

## 使用

查看会议和论文集：

```bash
python main.py list
python main.py list --conference acl
```

分析 ACL 2022–2025 年主会长文中的 knowledge 主题，与重构前 `main.py` 的默认分析对应：

```bash
python main.py trend --conference acl --years 2022 2023 2024 2025 --keywords knowledge
```

同时匹配多个关键词，并指定图表主题：

```bash
python main.py trend --conference iclr --years 2022 2023 2024 2025 --keywords llm lm --description "language model"
```

生成词云：

```bash
python main.py wordcloud --conference icml --year 2025 --max-words 150
```

年份选择默认采用当年的主会分卷，优先顺序为 `mainlong`、`main`、无后缀、`main&benchmark`。例如 ACL 2025 选择 `2025mainlong`，NeurIPS 2022 选择 `2022main&benchmark`。也可以指定分卷后缀或完整 ID：

```bash
python main.py trend --conference acl --years 2023 2024 --track findlong --keywords knowledge
python main.py trend --conference acl --proceedings 2020main 2021mainlong --keywords knowledge
python main.py wordcloud --conference nips --proceeding "2024main&benchmark"
```

趋势图按年份从早到晚展示；同一论文集重复传入只统计一次。`--track` 只与年份参数一起使用。关键词不区分大小写，短语使用引号包围。

图表默认只保存，不打开窗口；添加 `--show` 可在保存后显示。使用 `--output-dir` 修改输出位置，例如：

```bash
python main.py wordcloud --conference icml --year 2025 --output-dir outputs/demo --show
```

也可以在项目根目录运行 `python -m panaly ...`，参数完全相同。无参数时显示帮助，不再自动启动分析。

## 数据和输出

默认目录均相对于运行命令时的工作目录：

```text
data/
├── raw/<conference>/<proceeding>.html 或 .bib
└── processed/<conference>/
    ├── <proceeding>.json  # 原始标题、标准化标题、来源序号及源文件校验值
    └── <proceeding>.txt   # 标准化标题，供原有文本接口使用
outputs/
├── plot_acl_knowledge.png
├── trend_acl_knowledge_summary.csv
├── trend_acl_knowledge_papers.csv
├── trend_acl_knowledge_metadata.json
└── wordcloud_icml2025_top150.png
```

使用 `--data-dir` 修改数据目录。下载时优先使用 `data/raw` 中已有的文件，其次读取原有 `resources` 缓存，最后才下载。`--legacy-dir` 可指定旧缓存目录。旧缓存不会自动移动、删除或覆盖，提取的标题统一写入 `data/processed`，JSON 同时保留原始大小写、标点和排版换行；BibTeX 标题保留原有花括号，标准化时去掉这些标记。每次分析都会重新从原始文件提取标题，以应用当前术语配置。

缓存和图片已加入 `.gitignore`。分析图片统一保存在 `outputs`。

## 匹配规则与结果核查

标题和查询词先统一 Unicode 与大小写，再把标点、连字符、下划线作为词间分隔符。配置中的完整术语别名会归并，例如 `large-language-models` 与 `LLM` 等价；词内片段不会被匹配，例如 `reagents` 不再命中 `agent`。

多词查询匹配连续词元，不会跳过中间单词。除术语表中显式列出的变体外，不自动推断单复数或词干。示例：

```bash
python main.py trend --conference iclr --years 2022 2023 2024 2025 --keywords "knowledge graph" "knowledge graphs" LLM --description "selected topics"
```

`language model` 归并为 `LM`，`large language model` 归并为 `LLM`，二者分别匹配。如果要把 `MLLM` 和 `language modeling` 也算入语言模型主题，请显式加入这些关键词或配置对应别名。

每次通过 `trend` 或 `run_trend` 分析时，除图片外还会保存：

- `*_summary.csv`：各论文集的相关论文数、总数、占比（百分数）和查询词。
- `*_papers.csv`：每篇匹配论文的原始标题、标准化标题、命中关键词、论文集 URL 和源记录序号（从 1 开始）。一篇记录只占一行；等价查询合并，命中标签保留第一次传入的写法。
- `*_metadata.json`：本次输入、标准化查询、规则版本、术语表快照、源文件 SHA-256、时间和输出文件名。

CSV 使用 UTF-8 BOM 编码；包含逗号、引号或换行的标题会正确引用。`matched_keywords`、`keywords` 列的值是 JSON 数组。每个论文集的匹配明细行数等于统计表中的 `count`，原始记录总数作为分母；同名的不同源记录仍分别计数。

加上 `--compare-legacy` 可额外生成 `*_comparison.csv` 和 `*_changes.csv`：前者列出旧数、新数、增减数量和占比，后者逐篇给出变化方向、旧/新标准化标题、命中关键词和原因类别。

```bash
python main.py trend --conference iclr --years 2022 2023 2024 2025 --keywords knowledge --compare-legacy
```

对照里的 `title_normalization` 表示仅调整标题标准化就改变了命中结果；`query_normalization_or_phrase` 表示查询词归一化或短语匹配导致变化。旧规则使用冻结的第一轮术语表和原来的匹配方式；旧查询仍按当时的小写要求执行。

同一会议和描述的输出文件会覆盖，比较不同查询时请使用不同 `--description` 或 `--output-dir`。运行记录中的 `comparison_enabled` 和 `comparison_files` 指明本次是否生成对照文件。已有旧对照文件不会被自动删除。

旧版 `.txt` 不含原始标题，不能恢复原文。新分析会直接复用已有 HTML/BibTeX 重新提取；Python 读取接口也可以使用新的 JSON 缓存，并从原始标题重新应用当前术语规则。

## 项目结构

```text
panaly/
├── cli.py          # 参数解析与终端输出
├── config.py       # 每个论文集只配置一次：会议、ID、URL、解析方式
├── terminology.py  # 有序术语替换表和额外停用词
├── models.py       # 论文集和统计结果的数据类型
├── paths.py        # 路径生成与旧缓存查找
├── download.py     # 下载原始资源
├── parsers.py      # HTML / BibTeX 标题提取
├── normalize.py    # 标题和查询词使用同一套标准化规则
├── analysis.py     # 关键词/短语匹配、数量、占比及命中证据
├── export.py       # 统计表、匹配明细与运行记录
├── comparison.py   # 旧规则复现和逐篇差异说明
├── legacy_terms.json # 冻结的第一轮术语表，仅用于对照
├── plotting.py     # 绘图与保存
├── pipeline.py     # 组合完整分析流程
└── compat.py       # 原有 Python 导入接口的兼容层
tests/
├── fixtures/       # 小型解析样本及重构前结果快照
└── test_*.py       # 单元、CLI 和本地数据回归测试
```

新增论文集时，只需在 `panaly/config.py` 的对应会议和解析方式分组中添加一条 ID → URL 记录；新文件路径自动生成。会议 ID 为小写，论文集 ID 以四位年份开头。新增页面结构时，在 `parsers.py` 中添加相应解析器。

在 `panaly/terminology.py` 中调整术语和停用词。标题和查询词共用这份别名表，完整短语中更长的别名优先；替换只进行一遍，不连锁替换。`legacy_terms.json` 是第一轮对照快照，不是当前配置。

## Python 接口与迁移

新代码可以直接调用流程函数，获得结构化统计结果和输出路径：

```python
from pathlib import Path

from panaly.config import select_proceedings
from panaly.paths import Paths
from panaly.pipeline import run_trend

proceedings = select_proceedings("acl", years=[2022, 2023, 2024, 2025])
points, image_path = run_trend(
    proceedings,
    keywords=["knowledge"],
    description="knowledge",
    paths=Paths(output_dir=Path("outputs")),
)
for point in points:
    print(point.proceeding.key, point.count, point.total, point.ratio)
    for match in point.matches:
        print(match.paper.original_title, match.matched_keywords)
```

原有 `main.plot_tendency`、`main.plot_wordcloud`、`search_paper.PaperSearcher` 等导入保留为兼容入口，内部转交包实现。兼容入口同样默认保存到 `outputs`；绘图时可以显式传入 `show=True`。原有趋势接口继续按传入论文集的逆序绘图。

根目录 `config.Config` 的 URL 和路径字典是兼容读取快照，不再作为配置来源；修改配置请编辑包内 `config.py`。术语和停用词已移到 `terminology.py`。

`extract_keyword.py` 保留为原有的独立实验脚本，未接入默认流程。本轮未调整其 API 调用；它额外使用现有环境中的 `openai` 库，并需要完成原脚本的 API Key 配置。

## 验证与本轮边界

`pyproject.toml` 仅保存测试和代码格式检查的设置，不包含安装或构建配置。以下开发检查使用现有环境中的 pytest 和 Ruff，不是运行脚本的前置步骤。

```bash
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
```

测试保留第一轮证据，并独立核对第二轮结果：

- 全部 89 个论文集的 URL、解析方式和旧缓存文件名。
- 原始标题、Unicode、连字符、词边界、别名、连续短语及一篇只计一次。
- JSON 原文保留、旧缓存识别、CSV 转义和明细与统计表的一致性。
- 12 个本地论文集的源文件校验值、旧规则复现，以及 108 组新计数和占比。
- CLI 直接运行、旧 Python 入口和图表生成。

本地原始数据未提交到仓库；缺少对应 `resources` 文件时，该项回归测试会跳过，其他测试仍可运行。只运行不需要本地大数据的测试可执行 `python -m pytest -q -m "not local_data"`。

第一轮快照仍保存在 `tests/fixtures/local_baseline.json`，第二轮快照为 `tests/fixtures/phase2_baseline.json`；完整变化说明见 [匹配规则变更核查](docs/matching-changes.md)。词云使用新的标准化标题，因此内容和词频可能随新规则变化；旧规则的词频仍由测试复核。

下载重试、失败恢复、空解析结果处理和预设主题配置尚未在本轮改动。
