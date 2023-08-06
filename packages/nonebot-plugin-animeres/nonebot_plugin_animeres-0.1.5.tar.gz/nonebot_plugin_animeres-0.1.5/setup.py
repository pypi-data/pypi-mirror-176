# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_animeres']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'lxml>=4.9.1,<5.0.0',
 'nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot2>=2.0.0rc1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-animeres',
    'version': '0.1.5',
    'description': '动漫资源获取插件',
    'long_description': '# 动漫资源获取插件\n\n这个插件主要是网站爬取过来的数据，在使用命令进行搜索时候采用关键字的方式，比如`天气之子`这时搜索的是`天气之子`相关资源，如果获取的资源并不理想或者你只需要生肉（无字幕）资源时，你就需要用`天气之子 raw`或`天气之子 mkv`这种多个关键字空格方式进行获取，这种方式准确度会比直接用`天气之子`精准且效果好，建议采用多关键字的方式进行搜索。\n\n## 安装\n\n`nb plugin install nonebot-plugin-animeres`\n\n<details>\n  <summary>使用pip安装</summary>\n\n  `pip install nonebot-plugin-animeres`\n</details>\n\n- 命令\n  - `资源`、`动漫资源`\n- 参数\n  - `资源名称`\n\n## 配置参数\n\n```env\nCARTOON_PROXY=                        # 设置代理端口\nCARTOON_FORWARD=false                 # 合并转发的形式发送消息\nCARTOON_LENGTH=3                      # 每次发送的数量，用-1表示全部取出\nCARTOON_FORMANT="{title}\\n{magnet}"   # 发送的消息格式化\nCARTOON_ONESKIP=true                  # 当只有一个选项时跳过\n```\n\n### CARTOON_PROXY\n\n通过`CARTOON_PROXY`参数可以设置代理来加速资源的获取或者获取不到的情况\n\n### CARTOON_FORWARD\n\n用来发送合并消息\n\n![合并消息转发](image/forward.png)\n\n### CARTOON_FORMANT\n\n格式化字符串\n\n| 标签 | 说明 |\n|---|---|\n| title | 资源名称 |\n| tag | 资源标签类型 |\n| size | 资源大小 |\n| magnet | 种子链接 |\n',
    'author': 'MelodyKnit',
    'author_email': '2711402357@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
