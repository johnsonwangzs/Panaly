from openai import OpenAI
from config import Config


class KeywordExtractor:
    """使用LLM API提取题目关键词"""
    def __init__(self, model='kimi'):
        super().__init__()
        self.api_key = ''
        self.base_url = ''
        if model == 'kimi':
            self._init_kimi()
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )

    def _init_kimi(self):
        self.api_key = "sk-wZPSkmQPprJA2xLD0MDUSM09IEsAauoKIOe7Ie3sUBu8iBiO"
        self.base_url = "https://api.moonshot.cn/v1"

    def extract_keyword_kimi(self, titles: list) -> list:
        keywords = []
        for title in titles:
            completion = self.client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[
                    {"role": "system", "content": "你是一个自然语言处理领域的专家。"},
                    {"role": "user",
                     "content": f"列出这个论文题目中的英文关键词，将你的答案用逗号隔开：{title}"}
                ],
                temperature=0.,
            )
            keywords.append(completion.choices[0].message.content.strip())
            print(title.strip())
            print(completion.choices[0].message.content.strip())
        return keywords

    def _init_gpt(self):
        pass

    def extract_keyword_gpt(self):
        pass


def extract_keyword(conference, proceeding):
    with open(Config.title_file.get(conference).get(proceeding), 'r', encoding='utf-8') as f:
        title_list = f.readlines()

    ke = KeywordExtractor(model='kimi')
    keyword_list = ke.extract_keyword_kimi(title_list)

    with open(Config.keyword_file.get(conference).get(proceeding), 'w', encoding='utf-8') as f:
        for keyword in keyword_list:
            f.write(keyword + '\n')  # 每行写入从一个title提取出的若干keywords


if __name__ == '__main__':
    conference = 'acl'
    proceeding = '2024mainlong'

    extract_keyword(conference, proceeding)
