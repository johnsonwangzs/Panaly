import re

from config import Config


class PaperSearcher:
    def __init__(self, conf_proceedings: dict, keywords: list):
        self.conf_proceedings = conf_proceedings
        self.keywords = keywords

    def search(self):
        """按指定的关键字检索论文.
        不区分大小写, 必须完整匹配"""
        total = 0
        record = {}
        for conference in self.conf_proceedings.keys():
            if conference in Config.title_file.keys():
                record[conference] = {}
                for proceeding in self.conf_proceedings[conference]:
                    if proceeding in Config.title_file.get(conference).keys():
                        with open(Config.title_file.get(conference).get(proceeding), 'r', encoding='utf-8') as f:
                            titles = f.readlines()
                            record[conference][proceeding] = 0
                            for title in titles:
                                title_lower = title.lower()
                                title_split = re.split(r'[ -:]', title_lower)
                                contains_word = any(word in title_split for word in self.keywords)
                                if contains_word:
                                    print(conference + '-' + proceeding + ' | ' + title.strip())
                                    record[conference][proceeding] += 1
                                    total += 1
        return total, record


def search_paper(conf_proceedings, keywords):
    print(f'> 正在检索关键词:{keywords}...')
    ps = PaperSearcher(conf_proceedings, keywords)
    total, record = ps.search()
    print(f'----------------\n检索完成, 共找到 {total} 篇含关键字的论文.')
    print(record)
    return record


if __name__ == '__main__':
    conf_proceedings = {
        'acl': ['2024mainlong', '2024findlong'],
        'coling': ['2024main']
    }
    keywords = ['lm']

    search_paper(conf_proceedings, keywords)
