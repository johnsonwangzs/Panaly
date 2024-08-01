from search_paper import search_paper
import matplotlib.pyplot as plt
from config import Config
import numpy as np


class TendAnalyzer:
    def __init__(self, conf_proceedings: dict, keywords: list):
        self.conf_proceedings = conf_proceedings
        self.keywords = keywords

    def draw_plot(self, description, record):
        for conference in record.keys():
            proceedings = list(record[conference].keys())
            proceedings.reverse()
            paper_cnt = list(record[conference].values())
            paper_cnt.reverse()
            paper_cnt = np.array(paper_cnt)

            paper_total = []
            for proceeding in proceedings:
                with open(Config.title_file.get(conference).get(proceeding), 'r', encoding='utf-8') as f:
                    data = f.readlines()
                    paper_total.append(len(data))
            paper_total = np.array(paper_total)
            paper_ratio = paper_cnt / paper_total * 100.

            fig, ax1 = plt.subplots()  # 创建Y1轴
            ax1.plot(proceedings, paper_ratio, color='g', marker='o', label='占比')  # 折线图
            ax2 = ax1.twinx()
            ax2.bar(proceedings, paper_cnt, color='r', alpha=0.4, label='数量')  # 柱状图

            plt.title(f'Ratio & Number for [{description}]-related \nPapers in [{conference.upper()}] Proceedings')
            ax1.set_xlabel('Proceeding')
            ax1.set_ylabel('Keywords-related Paper / Total (%)')
            ax2.set_ylabel('Number')
            ax1.tick_params(axis='x', rotation=45, labelsize='small')  # 旋转45度，设置较小的字体大小

            print(f'X: 论文集{proceedings=}')
            print(f'Y1: 关键字相关论文占论文集总数{paper_ratio=}')
            print(f'Y2: 关键字相关论文数量{paper_cnt=}')

            plt.grid(True)  # 显示网格
            plt.tight_layout()

            save_path = 'plot_' + conference + '_' + description + '.png'
            plt.savefig(save_path)
            print('图表保存至 ' + save_path)

            plt.show()


def analyze_tendency(conf_proceedings, description, keywords):
    record = search_paper(conf_proceedings, keywords)
    print('> 正在绘图...')
    ta = TendAnalyzer(conf_proceedings, keywords)
    ta.draw_plot(description, record)
    print('绘图完成.')


if __name__ == '__main__':
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

    # 需提供关键字的各种可能变体(小写), 并指定图表描述文字
    # description = 'bias&fairness'
    # keywords = ['bias', 'biased', 'biases',
    #             'debias', 'debiased', 'debiasing', 'de-bias', 'de-biased', 'de-biasing',
    #             'fairness',]

    description = 'evaluation'
    keywords = ['evaluation',
                'benchmark',
                'metric', 'metrics',
                'dataset', 'datasets',
                'criterion',]

    # description = 'knowledge-graphs'
    # keywords = ['kg']

    # description = 'knowledge-distillation'
    # keywords = ['distill', 'distillation', 'distilling', 'distilled']

    # description = 'large-language-models'
    # keywords = ['llm']

    # description = 'generation'
    # keywords = ['generation']

    # description = 'dialogue'
    # keywords = ['dialog', 'dialogue']

    # description = 'vision'
    # keywords = ['vision', 'visual', 'visualize']

    # description = 'embedding'
    # keywords = ['embedding', 'embeddings', 'embed', 'embedded']

    analyze_tendency(conf_proceedings, description, keywords)
