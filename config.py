class Config:
    # 原始html文件
    src_file = {
        'acl': {
            '2024mainlong': 'resources/Accepted Main Conference Papers - ACL 2024.html',
            '2024findlong': 'resources/Accepted Findings Papers - ACL 2024.html',
            '2023mainlong': 'resources/2023.acl-long.bib',
            '2023findlong': 'resources/2023.findings-acl.bib',
            '2022mainlong': 'resources/2022.acl-long.bib',
            '2022findlong': 'resources/2022.findings-acl.bib',
            '2021mainlong': 'resources/2021.acl-long.bib',
            '2021findlong': 'resources/2021.findings-acl.bib',
            '2020main': 'resources/2020.acl-main.bib',
            '2019main': 'resources/P19-1.bib',
            '2018main': 'resources/P18-1.bib',
            '2017main': 'resources/P17-1.bib',
        },
        'emnlp': {
            '2023main': 'resources/2023.emnlp-main.bib',
            '2022main': 'resources/2022.emnlp-main.bib',
            '2021main': 'resources/2021.emnlp-main.bib',
            '2020main': 'resources/2020.emnlp-main.bib',
        },
        'coling': {
            '2024main': 'resources/2024.lrec-main.bib',
            '2022main': 'resources/2022.coling-1.bib',
            '2020main': 'resources/2020.coling-main.bib',
        },
        'nips': {
            '2023main': 'resources/2023.nips.htm',
            '2022main': 'resources/2022.nips.htm'
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
        },
        'emnlp': {
            '2023main': 'resources/title_emnlp23main.txt',
            '2022main': 'resources/title_emnlp22main.txt',
            '2021main': 'resources/title_emnlp21main.txt',
            '2020main': 'resources/title_emnlp20main.txt',
        },
        'coling': {
            '2024main': 'resources/title_coling24main.txt',
            '2022main': 'resources/title_coling22main.txt',
            '2020main': 'resources/title_coling20main.txt',
        },
        'nips': {
            '2023main': 'resources/title_nips23main.txt',
            '2022main': 'resources/title_nips22main.txt'
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
