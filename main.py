from config import Config
from extract_title import extract_title
from gen_wordcloud import gen_wordcloud
from analyze_tendency import analyze_tendency


max_words = 150  # 词云包含Top k高频词

# 在config.py中查看或添加会议和论文集
conference = 'acl'
proceeding = '2024main'

# 用于描述趋势.
# 指定论文集
# 需提供关键字的各种可能变体(小写), 并指定图表描述文字
conf_proceedings = {
    'acl':
        ['2024mainlong',
         '2023mainlong',
         '2022mainlong',
         '2021mainlong',
         '2020main',
         '2019main',
         '2018main',
         '2017main']
}
description = 'evaluation'
keywords = ['evaluation',
            'benchmark',
            'metric', 'metrics',
            'dataset', 'datasets',
            'criterion', ]


if __name__ == '__main__':
    # 绘制趋势图
    analyze_tendency(conf_proceedings, description, keywords)

    # 绘制词云
    extract_title(conference, proceeding)
    gen_wordcloud(conference, proceeding, max_words)
