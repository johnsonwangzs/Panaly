import wget
from config import Config
import os.path


class Downloader:
    def __init__(self, dl_target: dict):
        super().__init__()
        self.dl_target = dl_target

    def download_files(self):
        for conference in self.dl_target.keys():
            for proceeding in self.dl_target[conference]:
                file_name = Config.src_file.get(conference).get(proceeding)
                if os.path.exists(file_name):
                    print(f'本地已存在文件: {conference} 论文集 {proceeding}: {file_name}')
                else:
                    url = Config.src_url.get(conference).get(proceeding)
                    print(f'正在下载文件: {url}...')
                    wget.download(url, out=file_name)
                    print(f'已下载 {conference} 论文集 {proceeding} 至: {file_name}')


def dl_resource(conf_proceedings):
    print('> 正在下载所需资源...')
    dl = Downloader(conf_proceedings)
    dl.download_files()
    print('下载完毕.')


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


