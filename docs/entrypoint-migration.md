# 入口迁移与兼容窗口

本阶段统一使用 `python -m panaly` 和 `panaly.*` Python 接口，保留现有统计口径、论文集目录、缓存读取顺序及输出命名。这里只整理入口和依赖，不引入 Web 服务或改变分析流程。

## 兼容窗口

- 根目录旧 Python 导入从本次改动起弃用，计划在 **v1.0.0** 移除；这是兼容移除的计划版本，不代表本次发布 v1.0.0。
- v1.0.0 前保留根目录转发文件、旧函数签名及 `panaly.compat` 适配器。实际删除时需核对调用方迁移情况，并在发布说明中列出破坏性变更。
- `python main.py ...` 暂时保留为 CLI 启动兼容方式，其执行不会加载旧 Python 适配器。文档与帮助统一推荐 `python -m panaly ...`。
- 普通业务代码和实验脚本不再导入根目录旧模块。只有专门的兼容测试继续使用这些旧导入，验证过渡期可用性。

旧 Python 入口发出标准 `DeprecationWarning`，包含替代模块和本文档路径。Python 可能按默认过滤规则隐藏这类警告；迁移时可执行 `python -Wd your_script.py` 查看提示。

## 替代接口

下表是迁移方向，并非所有调用都只需修改 import；新接口使用 `Proceeding` 和 `Paths`，返回结构化数据，参数与返回值可能不同。

| 旧接口 | 推荐接口 |
|---|---|
| `main.plot_tendency` | `panaly.config.select_proceedings` + `panaly.pipeline.run_trend` |
| `main.plot_wordcloud` | `panaly.config.get_proceeding` + `panaly.pipeline.run_wordcloud` |
| `config.Config` | `panaly.config` 的论文集目录、`panaly.paths.Paths` 的路径方法、`panaly.terminology` 的术语配置 |
| `dl_resource.Downloader` / `dl_resource.dl_resource` | 对每个论文集调用 `panaly.download.download_source` |
| `extract_title.TitleExtractor` | `panaly.parsers.parse_papers`，输入文件内容和解析类型 |
| `extract_title.extract_title` | `panaly.pipeline.extract_papers`，解析已存在的原始资源并保存标题 |
| `extract_title.substitute_terminology` | `panaly.normalize.normalize_title` |
| `search_paper.PaperSearcher` / `search_paper.search_paper` | `panaly.pipeline.read_papers` + `panaly.analysis.analyze_papers` |
| `analyze_tendency.TendAnalyzer` / `analyze_tendency.analyze_tendency` | `read_papers` + `analyze_papers` + `panaly.plotting.plot_trend`；完整准备流程可用 `run_trend` |
| `gen_wordcloud.gen_wordcloud` | `panaly.pipeline.read_titles` + `panaly.plotting.plot_wordcloud`；完整准备流程可用 `run_wordcloud` |
| `utils.prepare_terminology` | `panaly.normalize.prepare_terminology` |
| `extract_keyword.KeywordExtractor` / `extract_keyword.extract_keyword` | `experiments.extract_keyword` 中的同名接口 |

需要短期保留原有函数签名的脚本可以显式使用 `panaly.compat`，但新增功能应使用上表的正式模块。旧趋势接口按输入逆序绘图；`select_proceedings` 按年份排序，迁移时应确认所需顺序。

## Python 调用示例

下载并提取一个论文集：

```python
from panaly.config import get_proceeding
from panaly.paths import Paths
from panaly.pipeline import prepare_papers

item = get_proceeding("acl", "2024mainlong")
papers = prepare_papers(item, Paths())
```

只分析已有数据，不执行下载或绘图：

```python
from panaly.analysis import analyze_papers
from panaly.config import get_proceeding
from panaly.paths import Paths
from panaly.pipeline import read_papers

item = get_proceeding("acl", "2024mainlong")
result = analyze_papers(item, read_papers(item, Paths()), ["knowledge"])
print(result.count, result.total, result.ratio)
for match in result.matches:
    print(match.paper.original_title, match.matched_keywords)
```

完整趋势分析示例见根目录 README 的 Python 接口部分。实验入口和配置见 [实验说明](../experiments/README.md)。

## 依赖划分

| 用途 | 安装命令 | 包含内容 |
|---|---|---|
| 正常分析 | `python -m pip install -r requirements.txt` | Beautiful Soup、BibTeX 解析、Matplotlib、WordCloud |
| 开发与验证 | `python -m pip install -r requirements-dev.txt` | 运行依赖及 pytest、Ruff |
| LLM 实验 | `python -m pip install -r experiments/requirements.txt` | 运行依赖及实验使用的可选 SDK |

以上命令在项目根目录执行，使用当前 Python 环境，不创建或切换虚拟环境。依赖文件按用途包含运行清单，避免重复维护其版本范围。`pyproject.toml` 继续只管理开发工具配置，项目仍可直接从源码运行。
