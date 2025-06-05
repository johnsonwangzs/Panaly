import re
from config import Config


def prepare_terminology():
    l = {}
    for terminology, variants in Config.tidy_terminology.items():
        # 转义并拼接所有变体
        pattern = r'|'.join([re.escape(v.lower()) for v in variants])
        # 编译为忽略大小写的正则对象
        l[terminology] = re.compile(pattern, flags=re.IGNORECASE)
    return l


if __name__ == '__main__':
    res = prepare_terminology()
    print(res)
