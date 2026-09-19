# 可选实验

此目录存放未接入默认分析流程的实验。核心 `panaly` 包不导入本目录，也不依赖实验 SDK。

## LLM 关键词提取

`extract_keyword.py` 从已有标题文本中逐篇提取关键词。它使用 `panaly.config` 和 `panaly.paths`，不再依赖根目录 `config.Config`。

在项目根目录安装可选依赖：

```bash
python -m pip install -r experiments/requirements.txt
```

通过环境变量配置：

| 变量 | 说明 |
|---|---|
| `MOONSHOT_API_KEY` | 必填，实验所用 API Key |
| `MOONSHOT_BASE_URL` | 可选，默认沿用原脚本的 `https://api.moonshot.cn/v1` |
| `MOONSHOT_MODEL` | 可选，默认沿用原脚本的 `moonshot-v1-8k`；可按账户可用模型覆盖 |

不再将凭据写入 Python 源文件。本次迁移未更换模型调用协议或提示词，也未验证远端模型可用性。

从项目根目录运行：

```bash
python -m experiments.extract_keyword --help
python -m experiments.extract_keyword --conference acl --proceeding 2024mainlong
```

未提供参数时仍选择 ACL 2024 主会长文。脚本先读取 `data/processed/<会议>/<论文集>.txt`，不存在时读取 `resources/title_*.txt`，不会自动下载或生成标题。可先使用核心的 `prepare_papers`、`trend` 或 `wordcloud` 准备数据。

输出沿用旧实验的 `resources/keyword_*.txt` 命名，例如 `resources/keyword_acl24mainlong.txt`，相同目标再次运行会覆盖。Python 调用 `extract_keyword(..., paths=Paths(...))` 可以指定数据和旧缓存目录。

根目录 `extract_keyword.py` 保留为弃用转发入口。模块导入和 `--help` 不需要可选 SDK 或 API Key；只有实际执行提取时才创建远端客户端。自动测试使用替身验证文件输入输出，不发送真实模型请求。
