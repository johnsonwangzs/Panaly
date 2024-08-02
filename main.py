from config import Config
from extract_title import extract_title
from gen_wordcloud import gen_wordcloud
from analyze_tendency import analyze_tendency
from dl_resource import dl_resource


max_words = 150  # 词云包含Top k高频词

# 在config.py中查看或添加会议和论文集
conference = 'nips'
proceeding = '2023main&benchmark'

# 用于描述趋势.
# 指定论文集
# 需提供关键字的各种可能变体(小写), 并指定图表描述文字
# conf_proceedings = {
#     'acl':
#         ['2024mainlong',
#          '2023mainlong',
#          '2022mainlong',
#          '2021mainlong',
#          '2020main',
#          '2019main',
#          '2018main',
#          '2017main']
# }
conf_proceedings = {
    'nips':
        ['2023main&benchmark',
         '2022main&benchmark',
         '2021main']
}
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
