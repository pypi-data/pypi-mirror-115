# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot', 'nonebot.adapters.feishu']

package_data = \
{'': ['*']}

install_requires = \
['aiocache>=0.11.1,<0.12.0',
 'httpx>=0.18.0,<0.19.0',
 'nonebot2>=2.0.0-alpha.14,<3.0.0',
 'pycryptodome>=3.10.1,<4.0.0']

setup_kwargs = {
    'name': 'nonebot-adapter-feishu',
    'version': '2.0.0a14',
    'description': 'feishu(larksuite) adapter for nonebot2',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# NoneBot-Adapter-Feishu\n\n_✨ 飞书协议适配 ✨_\n\n</div>\n',
    'author': 'StarHeartHunt',
    'author_email': 'starheart233@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://v2.nonebot.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
