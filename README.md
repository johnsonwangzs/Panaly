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

趋势图按年份从早到晚展示；同一论文集重复传入只统计一次。`--track` 只与年份参数一起使用。关键词需使用小写。

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
└── processed/<conference>/<proceeding>.txt
outputs/
├── plot_acl_knowledge.png
└── wordcloud_icml2025_top150.png
```

使用 `--data-dir` 修改数据目录。下载时优先使用 `data/raw` 中已有的文件，其次读取原有 `resources` 缓存，最后才下载。`--legacy-dir` 可指定旧缓存目录。旧缓存不会自动移动、删除或覆盖，提取的标题统一写入 `data/processed`。每次分析都会重新从原始文件提取标题，以应用当前术语配置。

缓存和图片已加入 `.gitignore`。根目录已有的历史图片仍然保留。

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
├── normalize.py    # 标题标准化
├── analysis.py     # 关键词匹配、数量与占比
├── plotting.py     # 绘图与保存
├── pipeline.py     # 组合完整分析流程
└── compat.py       # 原有 Python 导入接口的兼容层
tests/
├── fixtures/       # 小型解析样本及重构前结果快照
└── test_*.py       # 单元、CLI 和本地数据回归测试
```

新增论文集时，只需在 `panaly/config.py` 的对应会议和解析方式分组中添加一条 ID → URL 记录；新文件路径自动生成。会议 ID 为小写，论文集 ID 以四位年份开头。新增页面结构时，在 `parsers.py` 中添加相应解析器。

在 `panaly/terminology.py` 中调整术语和停用词。术语替换顺序沿用原代码，例如 LLM 必须先于 LM 处理。

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

测试快照从重构前的工作区代码实际运行生成，覆盖：

- 全部 89 个论文集的 URL、解析方式、旧缓存文件名和术语配置。
- HTML / BibTeX 小样本的标题提取结果。
- 本地 ACL、ICLR、ICML 各 2022–2025 年，共 12 个论文集的标题内容、9 组主题的数量和占比，以及词云前 150 词的词频和顺序。
- CLI 参数、目录选择、缓存复用和图表生成。

本地大数据未提交到仓库；缺少对应 `resources` 文件时，该项回归测试会跳过，其他测试仍可运行。要只运行无需本地大数据的测试，可执行 `python -m pytest -q -m "not local_data"`。替换已有源文件或有意调整统计规则时，需要评估并更新对应基线。

本轮保持原有分析口径：标题先按原顺序替换术语，检索时删除标点、转小写，再按完整 token 匹配任意关键词；一篇论文只计一次。多词短语、词边界改进、空数据处理和下载失败恢复留待下一轮。词云布局本身随机，回归比较词频而非逐像素图片。
