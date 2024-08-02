from config import Config
from extract_title import extract_title
from gen_wordcloud import gen_wordcloud
from analyze_tendency import analyze_tendency
from dl_resource import dl_resource

"""在config.py中查看或添加会议和论文集"""

"""设置用于构建词云的参数"""
max_words = 150  # 词云包含Top k高频词
conference = 'naacl'
proceeding = '2024mainlong'

"""设置用于绘制趋势的参数"""
# 指定论文集
conf_proceedings = {
    'naacl':
        ['2024mainlong',
         '2022mainlong',
         '2021mainlong',
         '2019mainlong',
         '2018mainlong',
         '2016main',
         '2015main',
         '2013main',
         '2012main',
         '2010main',
         ]
}

# 需提供关键字的各种可能变体(小写), 并指定图表描述文字
description = 'evaluation'
keywords = ['evaluation',
            'benchmark',
            'metric', 'metrics',
            'dataset', 'datasets',
            'criterion', ]


if __name__ == '__main__':
    # 绘制趋势图
    dl_resource(conf_proceedings)
    extract_title(conf_proceedings)
    analyze_tendency(conf_proceedings, description, keywords)

    print()

    # 绘制词云
    dl_resource({conference: [proceeding]})
    extract_title({conference: [proceeding]})
    gen_wordcloud(conference, proceeding, max_words)
