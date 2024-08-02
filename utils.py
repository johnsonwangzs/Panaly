from config import Config


def prepare_terminology():
    l = {}
    for terminology in Config.tidy_terminology.keys():
        l[terminology] = r'|'.join(list(map(lambda x: r'\b' + x.lower() + r'\b', Config.tidy_terminology[terminology])))
    return l


if __name__ == '__main__':
    res = prepare_terminology()
    print(res)
