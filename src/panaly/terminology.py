"""Ordered terminology aliases and additional wordcloud stop words."""

# Order matters: LLM aliases must be replaced before LM aliases.
TERMINOLOGY = {
    "LLM": ["llms", "llm-", "llm", "large language models", "large language model"],
    "pretrain": ["pre-trained", "pre-training", "pre-train", "pretrained", "pretraining"],
    "LM": ["language models", "language model"],
    "CoT": ["chain-of-thought"],
    "NLP": ["natural language processing"],
    "AI": ["artificial intelligence"],
    "InstTune": [
        "instruction tuning",
        "instruction tuned",
        "instruction-tuning",
        "instruction-tuned",
    ],
    "ReinLearn": ["reinforcement learning"],
    "ICL": ["in-context-learning", "in-context learning", "in context learning"],
    "finetune": ["fine-tuning", "fine-tuned", "fine-tune", "finetuning", "finetuned"],
    "evaluation": ["evaluating", "evaluated", "evaluate"],
    "benchmark": ["benchmarking", "benchmarks"],
    "watermark": ["watermarking", "watermarked", "watermarks"],
    "agent": ["agents", "multi-agent", "multi-agent", "-agent", "agent-", "agentic"],
}

STOP_WORDS = [
    "via",
    "based",
    "model",
    "models",
    "toward",
    "enhancing",
    "enhanced",
    "across",
    "beyond",
    "using",
    "exploring",
]
