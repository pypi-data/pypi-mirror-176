# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thu_learn_downloader']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'hydra-core>=1.2.0,<2.0.0',
 'python-slugify>=6.1.2,<7.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['build = thu_learn_downloader.build:run']}

setup_kwargs = {
    'name': 'thu-learn-downloader',
    'version': '0.1.0',
    'description': 'Auto download files from thu-learn',
    'long_description': '# thu-learn-downloader\n\nAuto download files from thu-learn\n\n## Demo\n\nSee Screen Recording at [demo.webm](https://drive.liblaf.top/github/thu-learn-downloader/demo.webm).\n\nThe resulting file structure looks like:\n\n```\nthu-learn\n└── engineering-mechanics-for-civil-engineering\n   ├── docs\n   │  ├── 作业与思考题\n   │  │  └── 第三周部分作业及思考题.pdf\n   │  ├── 电子教案\n   │  │  └── 第13讲-杆件拉伸和压缩.pdf\n   │  └── 课外阅读\n   │     └── 基于月面原位资源的月球基地建造技术.pdf\n   └── work\n      ├── 期中考试\n      │  └── README.md\n      └── 第2周作业\n         ├── attach-第2周作业.docx\n         ├── comment-2020012872-李钦-6544.pdf\n         ├── README.md\n         └── submit-第2周作业.pdf\n```\n\n## Features\n\n- pretty TUI powered by [rich](https://github.com/Textualize/rich)\n- auto set `mtime` of downloaded files according to timestamp of remote file\n- auto skip download when local file is newer\n- dump homework details into `README.md` in each homework folder\n- pretty markdown files powered by [prettier](https://prettier.io) (require `prettier` installed)\n\n## Usage\n\n1. Download pre-built binary from [releases](https://github.com/liblaf/thu-learn-downloader/releases).\n2. Prepare a `config.yaml` like [config.yaml](https://github.com/liblaf/thu-learn-downloader/blob/main/config.yaml).\n3. Run `thu-learn-downloader password="***"` and wait for the sync to finish.\n',
    'author': 'Qin Li',
    'author_email': 'liblaf@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://liblaf.github.io/thu-learn-downloader/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
