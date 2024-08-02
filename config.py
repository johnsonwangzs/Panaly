class Config:
    # 支持会议
    support_conference = ['acl', 'coling','emnlp', 'nips']

    # 网址
    src_url = {
        'acl': {  # https://aclanthology.org/venues/acl/
            '2024mainlong': 'https://2024.aclweb.org/program/main_conference_papers/',
            '2024findlong': 'https://2024.aclweb.org/program/finding_papers/',
            '2023mainlong': 'https://aclanthology.org/volumes/2023.acl-long.bib',
            '2023findlong': 'https://aclanthology.org/volumes/2023.findings-acl.bib',
            '2022mainlong': 'https://aclanthology.org/volumes/2022.acl-long.bib',
            '2022findlong': 'https://aclanthology.org/volumes/2022.findings-acl.bib',
            '2021mainlong': 'https://aclanthology.org/volumes/2021.acl-long.bib',
            '2021findlong': 'https://aclanthology.org/volumes/2021.findings-acl.bib',
            '2020main': 'https://aclanthology.org/volumes/2020.acl-main.bib',
            '2019main': 'https://aclanthology.org/volumes/P19-1.bib',
            '2018main': 'https://aclanthology.org/volumes/P18-1.bib',
            '2017main': 'https://aclanthology.org/volumes/P17-1.bib',
            '2016main': 'https://aclanthology.org/volumes/P16-1.bib',
            '2015main': 'https://aclanthology.org/volumes/P15-1.bib',
            '2014main': 'https://aclanthology.org/volumes/P14-1.bib',
            '2013main': 'https://aclanthology.org/volumes/P13-1.bib',
            '2012main': 'https://aclanthology.org/volumes/P12-1.bib',
            '2011main': 'https://aclanthology.org/volumes/P11-1.bib',
            '2010main': 'https://aclanthology.org/volumes/P10-1.bib',
        },
        'emnlp': {  # https://aclanthology.org/venues/emnlp/
            '2023main': 'https://aclanthology.org/volumes/2023.emnlp-main.bib',
            '2022main': 'https://aclanthology.org/volumes/2022.emnlp-main.bib',
            '2021main': 'https://aclanthology.org/volumes/2021.emnlp-main.bib',
            '2020main': 'https://aclanthology.org/volumes/D20-1.bib',
            '2019main': 'https://aclanthology.org/volumes/D19-1.bib',
            '2018main': 'https://aclanthology.org/volumes/D18-1.bib',
            '2017main': 'https://aclanthology.org/volumes/D17-1.bib',
            '2016main': 'https://aclanthology.org/volumes/D16-1.bib',
            '2015main': 'https://aclanthology.org/volumes/D15-1.bib',
            '2014main': 'https://aclanthology.org/volumes/D14-1.bib',
            '2013main': 'https://aclanthology.org/volumes/D13-1.bib',
            '2012main': 'https://aclanthology.org/volumes/D12-1.bib',
            '2011main': 'https://aclanthology.org/volumes/D11-1.bib',
            '2010main': 'https://aclanthology.org/volumes/D10-1.bib'
        },
        'coling': {  # https://aclanthology.org/venues/coling/
            '2024main': 'https://aclanthology.org/volumes/2024.lrec-main.bib',
            '2022main': 'https://aclanthology.org/volumes/2022.coling-1.bib',
            '2020main': 'https://aclanthology.org/volumes/2020.coling-main.bib',
            '2018main': 'https://aclanthology.org/volumes/C18-1.bib',
            '2016main': 'https://aclanthology.org/volumes/C16-1.bib',
            '2014main': 'https://aclanthology.org/volumes/C14-1.bib',
            '2012main': 'https://aclanthology.org/volumes/C12-1.bib',
            '2010main': 'https://aclanthology.org/volumes/C10-1.bib',
        },
        'nips': {
            '2023main&benchmark': 'https://papers.nips.cc/paper_files/paper/2023',
            '2022main&benchmark': 'https://papers.nips.cc/paper_files/paper/2022',
            '2021main': 'https://papers.nips.cc/paper_files/paper/2021',
            '2021benchmark': 'https://datasets-benchmarks-proceedings.neurips.cc/paper/2021',
        }
    }

    # 原始html/bib文件
    src_file = {
        'acl': {
            '2024mainlong': 'resources/2024.acl.main.html',
            '2024findlong': 'resources/2024.acl.findings.html',
            '2023mainlong': 'resources/2023.acl.main.bib',
            '2023findlong': 'resources/2023.acl.findings.bib',
            '2022mainlong': 'resources/2022.acl.main.bib',
            '2022findlong': 'resources/2022.acl.findings.bib',
            '2021mainlong': 'resources/2021.acl.main.bib',
            '2021findlong': 'resources/2021.acl.findings.bib',
            '2020main': 'resources/2020.acl.main.bib',
            '2019main': 'resources/2019.acl.main.bib',
            '2018main': 'resources/2018.acl.main.bib',
            '2017main': 'resources/2017.acl.main.bib',
            '2016main': 'resources/2016.acl.main.bib',
            '2015main': 'resources/2015.acl.main.bib',
            '2014main': 'resources/2014.acl.main.bib',
            '2013main': 'resources/2013.acl.main.bib',
            '2012main': 'resources/2012.acl.main.bib',
            '2011main': 'resources/2011.acl.main.bib',
            '2010main': 'resources/2010.acl.main.bib',
        },
        'emnlp': {
            '2023main': 'resources/2023.emnlp.main.bib',
            '2022main': 'resources/2022.emnlp.main.bib',
            '2021main': 'resources/2021.emnlp.main.bib',
            '2020main': 'resources/2020.emnlp.main.bib',
            '2019main': 'resources/2019.emnlp.main.bib',
            '2018main': 'resources/2018.emnlp.main.bib',
            '2017main': 'resources/2017.emnlp.main.bib',
            '2016main': 'resources/2016.emnlp.main.bib',
            '2015main': 'resources/2015.emnlp.main.bib',
            '2014main': 'resources/2014.emnlp.main.bib',
            '2013main': 'resources/2013.emnlp.main.bib',
            '2012main': 'resources/2012.emnlp.main.bib',
            '2011main': 'resources/2011.emnlp.main.bib',
            '2010main': 'resources/2010.emnlp.main.bib',
        },
        'coling': {
            '2024main': 'resources/2024.coling.main.bib',
            '2022main': 'resources/2022.coling.main.bib',
            '2020main': 'resources/2020.coling.main.bib',
            '2018main': 'resources/2018.coling.main.bib',
            '2016main': 'resources/2016.coling.main.bib',
            '2014main': 'resources/2014.coling.main.bib',
            '2012main': 'resources/2012.coling.main.bib',
            '2010main': 'resources/2010.coling.main.bib',
        },
        'nips': {
            '2023main&benchmark': 'resources/2023.nips.main&benchmark.htm',
            '2022main&benchmark': 'resources/2022.nips.main&benchmark.htm',
            '2021main': 'resources/2021.nips.main.htm',
            '2021benchmark': 'resources/2021.nips.benchmark.htm'
        }
    }

    # 提取的标题文件
    title_file = {
        'acl': {
            '2024mainlong': 'resources/title_acl24mainlong.txt',
            '2024findlong': 'resources/title_acl24findlong.txt',
            '2023mainlong': 'resources/title_acl23mainlong.txt',
            '2023findlong': 'resources/title_acl23findlong.txt',
            '2022mainlong': 'resources/title_acl22mainlong.txt',
            '2022findlong': 'resources/title_acl22findlong.txt',
            '2021mainlong': 'resources/title_acl21mainlong.txt',
            '2021findlong': 'resources/title_acl21findlong.txt',
            '2020main': 'resources/title_acl20main.txt',
            '2019main': 'resources/title_acl19main.txt',
            '2018main': 'resources/title_acl18main.txt',
            '2017main': 'resources/title_acl17main.txt',
            '2016main': 'resources/title_acl16main.txt',
            '2015main': 'resources/title_acl15main.txt',
            '2014main': 'resources/title_acl14main.txt',
            '2013main': 'resources/title_acl13main.txt',
            '2012main': 'resources/title_acl12main.txt',
            '2011main': 'resources/title_acl11main.txt',
            '2010main': 'resources/title_acl10main.txt',
        },
        'emnlp': {
            '2023main': 'resources/title_emnlp23main.txt',
            '2022main': 'resources/title_emnlp22main.txt',
            '2021main': 'resources/title_emnlp21main.txt',
            '2020main': 'resources/title_emnlp20main.txt',
            '2019main': 'resources/title_emnlp19main.txt',
            '2018main': 'resources/title_emnlp18main.txt',
            '2017main': 'resources/title_emnlp17main.txt',
            '2016main': 'resources/title_emnlp16main.txt',
            '2015main': 'resources/title_emnlp15main.txt',
            '2014main': 'resources/title_emnlp14main.txt',
            '2013main': 'resources/title_emnlp13main.txt',
            '2012main': 'resources/title_emnlp12main.txt',
            '2011main': 'resources/title_emnlp11main.txt',
            '2010main': 'resources/title_emnlp10main.txt',
        },
        'coling': {
            '2024main': 'resources/title_coling24main.txt',
            '2022main': 'resources/title_coling22main.txt',
            '2020main': 'resources/title_coling20main.txt',
            '2018main': 'resources/title_coling18main.txt',
            '2016main': 'resources/title_coling16main.txt',
            '2014main': 'resources/title_coling14main.txt',
            '2012main': 'resources/title_coling12main.txt',
            '2010main': 'resources/title_coling10main.txt',
        },
        'nips': {
            '2023main&benchmark': 'resources/title_nips23main&benchmark.txt',
            '2022main&benchmark': 'resources/title_nips22main&benchmark.txt',
            '2021main': 'resources/title_nips21main.txt',
            '2021benchmark': 'resources/title_nips21benchmark.txt'
        }
    }

    # 提取的关键词文件
    keyword_file = {
        'acl': {
            '2024mainlong': 'resources/keyword_acl24mainlong.txt',
            '2024findlong': 'resources/keyword_acl24findlong.txt'
        }
    }

    # TODO: 允许自定义专业术语
