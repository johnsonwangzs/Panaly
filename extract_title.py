import re
from config import Config
from bs4 import BeautifulSoup
import bibtexparser
from utils import prepare_terminology


def substitute_terminology(string):
    mod_string = string
    pattern_dict = prepare_terminology()
    for pattern in pattern_dict:
        mod_string = re.sub(pattern_dict[pattern], pattern, mod_string)
    # pattern = r'\blarge language model\b|\blarge language models\b|\bllm\b|\bllms\b|\bLLMs\b'
    # mod_string = re.sub(pattern, 'LLM', mod_string)
    # pattern = r'\bpre-trained\b|\bpre-training\b|\bpre-train\b|\bpretraining\b|\bpretrained\b'
    # mod_string = re.sub(pattern, 'pretrain', mod_string)
    # pattern = r'\blanguage model\b|\blanguage models\b'
    # mod_string = re.sub(pattern, 'LM', mod_string)
    # pattern = r'\bchain-of-thought\b'
    # mod_string = re.sub(pattern, 'CoT', mod_string)
    # pattern = r'\bnatural language processing\b'
    # mod_string = re.sub(pattern, 'NLP', mod_string)
    # pattern = r'\bartificial intelligence\b|\bai\b'
    # mod_string = re.sub(pattern, 'AI', mod_string)
    # pattern = r'\binstruction tuning\b'
    # mod_string = re.sub(pattern, 'InstTune', mod_string)
    # pattern = r'\bknowledge graph\b|\bknowledge graphs\b'
    # mod_string = re.sub(pattern, 'KG', mod_string)
    # pattern = r'\breinforcement learning\b'
    # mod_string = re.sub(pattern, 'RL', mod_string)
    # pattern = r'\bin-context learning\b|\bin context learning\b'
    # mod_string = re.sub(pattern, 'ICL', mod_string)
    # pattern = r'\bfine-tuning\b|\bfine-tuned\b|\bfine-tune\b'
    # mod_string = re.sub(pattern, 'finetuning', mod_string)
    # pattern = r'\bevaluating\b|\bevaluate\b'
    # mod_string = re.sub(pattern, 'evaluation', mod_string)
    # pattern = r'\bbenchmarking\b|\bbenchmarks\b'
    # mod_string = re.sub(pattern, 'benchmark', mod_string)
    return mod_string


class TitleExtractor:
    def __init__(self, conference, proceeding,):
        super().__init__()
        self.conference = conference
        self.proceeding = proceeding

    def extract_title_from_html_nips(self, file_path):
        """从 nips.cc 的html网页中获取论文题目
        例如 https://papers.nips.cc/paper_files/paper/2023"""
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        bs = BeautifulSoup(html_content, 'html.parser')
        ul_tags = bs.select('div.container-fluid ul')

        titles = []
        if ul_tags:
            ul_tag = ul_tags[0]
            li_tags = ul_tag.find_all('li')
            for li in li_tags:
                a_tag = li.find('a')
                if a_tag:
                    title = re.sub(r'\s+', ' ', a_tag.text).lower()  # 删除多余字符, 转小写
                    title = substitute_terminology(title)  # 专业术语合并
                    titles.append(title)
        else:
            print('No <ul> tag found with the specified selector.')

        print(f'提取完毕. {self.conference}-{self.proceeding}总数:', len(titles))
        return titles

    def extract_title_from_html_aclweb(self, file_path):
        """从 aclweb.org 的html网页中获取论文题目
        例如 https://2024.aclweb.org/program/main_conference_papers/ """
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()  # 读取原始html文件

        bs = BeautifulSoup(html_content, 'html.parser')
        # 定位特定的<ul>标签，使用BeautifulSoup的选择器
        ul_tags = bs.select('section.page__content ul')

        # 如果找到了<ul>标签，处理其中的<li>标签
        titles_long = []  # 仅统计长文
        if ul_tags:
            ul_tag = ul_tags[1]  # 仅统计主会长文
            li_tags = ul_tag.find_all('li')
            for li in li_tags:
                strong_tag = li.find('strong')
                if strong_tag:
                    title = re.sub(r'\s+', ' ', strong_tag.text).lower()  # 删除多余字符, 转小写
                    title = substitute_terminology(title)  # 专业术语合并
                    titles_long.append(title)
        else:
            print('No <ul> tag found with the specified selector.')

        print(f'提取完毕. {self.conference}-{self.proceeding}总数:', len(titles_long))
        return titles_long

    def extract_title_from_html_iclr(self, file_path):
        """从 iclr.cc 的html网页中获取论文题目
        例如 https://iclr.cc/Downloads/2024 """
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        bs = BeautifulSoup(html_content, 'html.parser')
        ul_tags = bs.select('div.list_html ul')

        titles = []
        if ul_tags:
            ul_tag = ul_tags[0]
            li_tags = ul_tag.find_all('li')
            for li in li_tags:
                a_tag = li.find('a')
                if a_tag:
                    title = re.sub(r'\s+', ' ', a_tag.text).lower()  # 删除多余字符, 转小写
                    title = substitute_terminology(title)  # 专业术语合并
                    titles.append(title)
        else:
            print('No <ul> tag found with the specified selector.')

        print(f'提取完毕. {self.conference}-{self.proceeding}总数:', len(titles))
        return titles

    def extract_title_from_bib(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            bib_data = bibtexparser.load(f)

        titles = []
        for entry in bib_data.entries:
            title = entry.get('title')
            title = re.sub(r'{(.*?)}', r'\1', title)
            title = re.sub(r'\s+', ' ', title).lower()  # 删除多余字符, 转小写
            title = substitute_terminology(title)  # 专业术语合并
            titles.append(title)

        print(f'提取完毕. {self.conference}-{self.proceeding}总数:', len(titles))
        return titles


def extract_title(conf_proceedings):
    print('> 正在提取标题...')
    for conference in conf_proceedings.keys():
        for proceeding in conf_proceedings[conference]:
            srcfile_path = Config.src_file.get(conference).get(proceeding)

            te = TitleExtractor(conference, proceeding)
            if conference in ['acl', 'emnlp', 'naacl', 'coling']:
                if srcfile_path.endswith('.html'):
                    title_list = te.extract_title_from_html_aclweb(srcfile_path)
                elif srcfile_path.endswith('.bib'):
                    title_list = te.extract_title_from_bib(srcfile_path)
            elif conference in ['nips']:
                if srcfile_path.endswith('.htm'):
                    title_list = te.extract_title_from_html_nips(srcfile_path)
            elif conference in ['iclr']:
                if srcfile_path.endswith('.html'):
                    title_list = te.extract_title_from_html_iclr(srcfile_path)

            with open(Config.title_file.get(conference).get(proceeding), 'w', encoding='utf-8') as f:
                for title in title_list:
                    f.write(title + '\n')


if __name__ == '__main__':
    conference = 'nips'
    proceeding = '2022main'

    extract_title({conference: [proceeding]})
