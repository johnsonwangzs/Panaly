# 第二轮匹配规则变更核查

本报告使用与第一轮完全相同的 12 个本地原始资源（ACL、ICLR、ICML 各 2022–2025 年）。源文件 SHA-256、提取数量、旧规则生成的标题以及旧计数全部对上第一轮冻结基线；因此以下差异来自匹配规则变化。

共 22,298 条论文记录、9 组主题、108 组会议年度统计。统计按论文记录计数，同一篇命中多个关键词仍计一次；同一篇在不同主题中可以重复出现。

## 规则变化

- 标题和查询词使用相同的大小写、Unicode 和术语别名归一化。
- 标点、连字符和下划线作为词间分隔符，不再删除后把相邻单词拼在一起。
- 术语按完整词或连续短语匹配，最长别名优先、单次替换，避免单词内部误替换。
- 多词查询匹配连续词元；不做任意词干推断。`LM` 与 `LLM` 是不同术语，需要分别传入才同时统计。

## 按主题汇总

以下为 12 个论文集的相关论文数量之和。新增和移除可能在不同论文上同时发生，净变化为二者之差。

| 主题 | 旧计数 | 新计数 | 新增 | 移除 | 净变化 |
|---|---:|---:|---:|---:|---:|
| knowledge | 505 | 564 | 59 | 0 | 59 |
| language_model | 3394 | 3283 | 6 | 117 | -111 |
| agent | 583 | 583 | 0 | 0 | 0 |
| watermark | 75 | 75 | 0 | 0 | 0 |
| reason | 563 | 575 | 12 | 0 | 12 |
| evaluation | 1423 | 1445 | 22 | 0 | 22 |
| safety | 604 | 647 | 43 | 0 | 43 |
| diffusion | 865 | 930 | 65 | 0 | 65 |
| graph | 980 | 1052 | 72 | 0 | 72 |

## 语言模型统计范围的变化

`language_model` 使用的查询是 `llm lm`。新规则下，`MLLM` / `MLLMs`、`language modeling` 以及 `FocusLLM` 一类完整模型名称不再通过单词内部替换而隐式命中。这些论文可能仍与语言模型相关，因此不能把所有移除项解释为语义上的误报。

若需要把前两类纳入统计，可显式使用 `--keywords llm lm mllm mllms "language modeling" "language modelling"`，或在当前术语表中添加你认可的别名。复合模型名称需要显式关键词或别名；本轮不增加任意子串检索。基线保持原查询与原别名表，以单独展示规则变化。

## 各论文集的计数变化

单元格为“旧 → 新”。

| 会议 / 论文集 | knowledge | language_model | agent | watermark | reason | evaluation | safety | diffusion | graph |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| acl/2025mainlong | 103 → 116 | 768 → 757 | 105 → 105 | 9 → 9 | 128 → 129 | 300 → 301 | 97 → 104 | 7 → 10 | 42 → 47 |
| acl/2024mainlong | 48 → 56 | 395 → 388 | 34 → 34 | 8 → 8 | 58 → 59 | 135 → 136 | 39 → 46 | 5 → 5 | 22 → 24 |
| acl/2023mainlong | 63 → 71 | 124 → 118 | 2 → 2 | 2 → 2 | 46 → 46 | 111 → 113 | 15 → 16 | 6 → 6 | 31 → 39 |
| acl/2022mainlong | 37 → 40 | 60 → 56 | 1 → 1 | 0 → 0 | 15 → 17 | 61 → 62 | 6 → 7 | 0 → 0 | 28 → 29 |
| iclr/2025 | 66 → 74 | 760 → 734 | 136 → 136 | 14 → 14 | 95 → 98 | 283 → 288 | 140 → 153 | 261 → 285 | 141 → 150 |
| iclr/2024 | 34 → 35 | 318 → 303 | 40 → 40 | 10 → 10 | 40 → 42 | 129 → 130 | 43 → 45 | 154 → 165 | 110 → 115 |
| iclr/2023 | 25 → 28 | 59 → 52 | 24 → 24 | 0 → 0 | 26 → 26 | 47 → 50 | 20 → 22 | 47 → 50 | 94 → 101 |
| iclr/2022 | 11 → 12 | 24 → 20 | 16 → 16 | 0 → 0 | 13 → 13 | 25 → 25 | 8 → 8 | 13 → 15 | 60 → 66 |
| icml/2025 | 52 → 61 | 503 → 487 | 115 → 115 | 16 → 16 | 95 → 98 | 171 → 173 | 143 → 145 | 182 → 193 | 158 → 175 |
| icml/2024 | 34 → 37 | 305 → 298 | 58 → 58 | 11 → 11 | 29 → 29 | 83 → 85 | 64 → 68 | 113 → 119 | 122 → 128 |
| icml/2023 | 20 → 21 | 59 → 54 | 32 → 32 | 4 → 4 | 12 → 12 | 43 → 44 | 15 → 16 | 65 → 70 | 108 → 110 |
| icml/2022 | 12 → 13 | 19 → 16 | 20 → 20 | 1 → 1 | 6 → 6 | 35 → 38 | 14 → 17 | 12 → 12 | 64 → 68 |

## 逐篇核查

`outputs/phase2/comparison_summary.csv` 包含完整 108 行统计、数量和占比；`outputs/phase2/changed_papers.csv` 包含全部增减论文的原始标题、旧标准化标题、新标准化标题、命中关键词、来源和原因类别。这两个文件是本地生成结果。

原因分类通过分步对照确定：先只替换标题标准化、保留旧检索器；再启用查询词归一化和短语匹配。`title_normalization` 表示第一步改变了结果，`query_normalization_or_phrase` 表示第二步改变了结果。类别说明规则触发点，不代替论文内容相关性的人工判断。

以下是实际变化示例：

- acl/2025mainlong，language_model，removed：PunchBench: Benchmarking MLLMs in Multimodal Punchline Comprehension
  - 旧：`punchbench: benchmark m LLM in multimodal punchline comprehension`
  - 新：`punchbench benchmark mllms in multimodal punchline comprehension`
  - 类别：`title_normalization`
- acl/2025mainlong，knowledge，added：Enhancing Unsupervised Sentence Embeddings via Knowledge-Driven Data Augmentation and Gaussian-Decayed Contrastive Learning
  - 旧：`enhancing unsupervised sentence embeddings via knowledge-driven data augmentation and gaussian-decayed contrastive learning`
  - 新：`enhancing unsupervised sentence embeddings via knowledge driven data augmentation and gaussian decayed contrastive learning`
  - 类别：`title_normalization`
- acl/2025mainlong，language_model，added：Enhancing Neural Machine Translation Through Target Language Data: A $k$NN-LM Approach for Domain Adaptation
  - 旧：`enhancing neural machine translation through target language data: a $k$nn-lm approach for domain adaptation`
  - 新：`enhancing neural machine translation through target language data a k nn LM approach for domain adaptation`
  - 类别：`title_normalization`
- acl/2025mainlong，reason，added：Micro-Act: Mitigate Knowledge Conflict in Question Answering via Actionable Self-Reasoning
  - 旧：`micro-act: mitigate knowledge conflict in question answering via actionable self-reasoning`
  - 新：`micro act mitigate knowledge conflict in question answering via actionable self reasoning`
  - 类别：`title_normalization`

## 复核方式

可在任意趋势命令后加 `--compare-legacy`，生成该主题的旧规则对照表和增减明细。例如：

```bash
python -m panaly trend --conference acl --years 2022 2023 2024 2025 --keywords knowledge --compare-legacy
```

第一轮基线保留在 `tests/fixtures/local_baseline.json`，新计数保存在 `tests/fixtures/phase2_baseline.json`。自动测试同时校验源文件、旧规则复现和新规则结果，不用新快照覆盖旧证据。
