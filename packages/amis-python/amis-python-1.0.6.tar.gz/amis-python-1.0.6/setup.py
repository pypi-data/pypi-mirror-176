# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amis']

package_data = \
{'': ['*'], 'amis': ['templates/*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0', 'pydantic>=1.9.2,<2.0.0']

setup_kwargs = {
    'name': 'amis-python',
    'version': '1.0.6',
    'description': '基于百度amis前端框架的python pydantic模型封装。',
    'long_description': '## amis-python\n<p align="center">\n    <a href="https://cdn.jsdelivr.net/gh/CMHopeSunshine/amis-python@master/LICENSE"><img src="https://img.shields.io/github/license/CMHopeSunshine/amis-python" alt="license"></a>\n    <img src="https://img.shields.io/badge/Python-3.7+-yellow" alt="python">\n    <img src="https://img.shields.io/pypi/v/amis-python" alt="version">\n</p>\n\n基于 [百度amis](https://github.com/baidu/amis) 前端框架的python pydantic模型封装。\n\n由于[原版本](https://github.com/amisadmin/fastapi_amis_admin/tree/master/fastapi_amis_admin/amis)缺少大量amis新版本的组件或配置，因此本项目在其版本的基础上进行了扩充。\n\n相比fastapi-amis-admin的版本：\n- 涵盖amis截至2.3.1版本的所有组件\n- 使用jinja2模板\n- 支持修改主题\n## 安装\n```\npip install amis-python\n```\n## 简单使用\n```python\nfrom amis.components import Page\n\npage = Page(title=\'新页面\', body=\'Hello World\')\n# 输出为python字典\nprint(page.to_dict())\n# 输出为json\nprint(page.to_json())\n# 输出为str\nprint(page.render())\n# 保存为html文件\nwith open(\'HelloWorld.html\', \'w\', encoding=\'utf-8\') as f:\n    f.write(page.render())\n```\n\n## 详细使用\n详见[amis官方文档](https://aisuda.bce.baidu.com/amis/zh-CN/docs/index)\n\n## 感谢\n- [amis](https://github.com/baidu/amis)\n- [fastapi-amis-admin](https://github.com/amisadmin/fastapi_amis_admin/tree/master/fastapi_amis_admin/amis)\n',
    'author': '惜月',
    'author_email': '277073121@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CMHopeSunshine/amis-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
