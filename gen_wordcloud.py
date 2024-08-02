import matplotlib.pyplot as plt
from wordcloud import WordCloud
from config import Config

max_words = 150
conference = 'nips'
proceeding = '2023main&benchmark'


def gen_wordcloud(conference: str, proceeding: str, max_words: int):
    """生成词云"""
    print('> 正在生成词云图片...')
    text = ''  # 所有涉及文本拼接成一个字符串
    with open(Config.title_file.get(conference).get(proceeding), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            text = text + ', ' + line

    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=max_words).generate(text)

    plt.figure(figsize=(10, 5), dpi=500)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    save_path = 'wordcloud_' + conference + proceeding + '_top' + str(max_words) + '.png'
    plt.savefig(save_path, dpi=500)
    print('词云图片保存至 ' + save_path)

    plt.show()


if __name__ == '__main__':
    gen_wordcloud(conference, proceeding, max_words)
