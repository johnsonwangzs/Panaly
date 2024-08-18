# Panaly

主要功能: 一键下载、提取、整理论文主题, 查看会议热点和领域发展趋势.

当前覆盖会议: [acl, coling, emnlp, iclr, icml, naacl, nips].

## 个性化配置

在`config.py`中进行全局配置:
- `tidy_terminology`: 专业术语聚合(会在标题和词云中进行相应替换), 影响词云的生成和趋势的统计.

在`main.py`中设置:
- 用于构建词云的参数
  - `max_words`: 词云包含的最大词数目.
  - `conference`: (1个)会议名.
  - `proceeding`: (1个)论文集名.

- 用于绘制趋势的参数
  - `conf_proceedings`: 指定(1个)会议和其下多个论文集.
  - `keywords`: 一个列表, 趋势图会统计含列表中任意词的论文.
  - `desctiption`: 描述(例如主题), 将出现在趋势图的标题中.

## 更多配置

在`config.py` 中添加更多会议和论文集. 格式可参考该python文件内容.

## 报错提示

1. 若下载或提取标题模块报错, 可能涉及的会议论文列表发布页面链接有改动, 此时手动将新的 url 更新到 `config.py` 相应位置即可.

    注意: 可能需要同时更新 `Config.src_url` 和 `Config.src_file` 中的内容

2. 若 wordcloud 包报错: "wordcloud Only supported for TrueType fonts", 按以下命令更新相关包即可:

```bash
pip install --upgrade pip 
pip install --upgrade Pillow
```

> https://stackoverflow.com/questions/76129498/wordcloud-only-supported-for-truetype-fonts